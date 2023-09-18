# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

import datetime

from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from rpc.models import DatatrackerPerson


class RpcOIDCAuthBackend(OIDCAuthenticationBackend):
    """Customized OIDC auth backend

    Assumes the datatracker makes the following claims:
      sub - pk of the Person who was authenticated, as a string
      name - plain_name of the Person identified by sub
      roles - list of 2-tuples corresponding to Person's active roles
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subject_id = None  # subject ID we are working with
        self.OIDC_OP_ISSUER_ID = self.get_settings("OIDC_OP_ISSUER_ID")

    def create_user(self, claims):
        """Create a User following a successful auth"""
        subject_id = claims["sub"]
        # A DatatrackerPerson may exist without a user so use get_or_create()
        datatracker_person, _ = DatatrackerPerson.objects.get_or_create(
            subject_id=subject_id,
            plain_name=claims.get("name", ""),
        )
        try:
            # Rely on the OneToOne field to avoid creating duplicate Users for a DatatrackerPerson
            new_user = self.UserModel.objects.create(
                username=f"dt-person-{subject_id}",
                datatracker_person=datatracker_person,
            )
        except IntegrityError:
            # exception message gets logged - user only sees a failed auth
            raise SuspiciousOperation(
                f"User already exists for datatracker person pk={subject_id}"
            )
        return new_user

    def update_user(self, user, claims):
        """Update a User following a successful auth"""
        # Update the name if we got it
        plain_name = claims.get("name", None)
        if plain_name is not None and plain_name != user.datatracker_person.plain_name:
            user.datatracker_person.plain_name = plain_name
            user.datatracker_person.save()
        return user

    def filter_users_by_claims(self, claims):
        """Return list or queryset of users who satisfy claims

        If the set does not have exactly one member, auth will be rejected.
        """
        # Only consider users who have a datatracker_person!
        return self.UserModel.objects.filter(
            datatracker_person__subject_id__isnull=False,
            datatracker_person__subject_id=claims["sub"],  # claim guaranteed to exist
        )

    def verify_token(self, token, **kwargs):
        """Verify the ID token"""
        payload = super().verify_token(token, **kwargs)
        # Validation mandated by sect 3.1.3.7 of the spec not performed by base backend class
        issuer_id = payload.get("iss", None)
        if issuer_id is None or issuer_id != self.OIDC_OP_ISSUER_ID:
            raise SuspiciousOperation(
                'issuer "{}" does not match configured issuer "{}"'.format(
                    issuer_id, self.OIDC_OP_ISSUER_ID
                )
            )
        # Check audience. Per spec, we must reject the token if it "does not list the Client as a
        # valid audience, or if it contains additional audiences not trusted by the Client." We only
        # expect one audience from the datatracker, so let's assume any other audiences are untrusted.
        audience = payload.get("aud", [])
        if isinstance(audience, str):
            audience = [audience]
        if len(set(audience)) != 1 or audience[0] != self.OIDC_RP_CLIENT_ID:
            raise SuspiciousOperation(
                'token has invalid audience "{}"'.format(audience)
            )
        # azp should be present if token contains multiple audiences, but we rejected such a token already.
        # Just check that, if present, azp is us
        if "azp" in payload and payload["azp"] != self.OIDC_RP_CLIENT_ID:
            raise SuspiciousOperation(
                'token azp ("{}") is not our client id ("{}")'.format(
                    payload["azp"], self.OIDC_RP_CLIENT_ID
                )
            )

        if "exp" not in payload:
            raise SuspiciousOperation("token has no expiration time")
        if not isinstance(payload["exp"], int):
            raise SuspiciousOperation(
                'token exp ("{}") is not an integer'.format(payload["exp"])
            )
        expiration_time = datetime.datetime.fromtimestamp(
            payload["exp"], tz=datetime.timezone.utc
        )
        if expiration_time < datetime.datetime.now(tz=datetime.timezone.utc):
            raise SuspiciousOperation(f"token expired at {expiration_time}")

        # remember the subject ID so we can validate claims later
        if "sub" in payload:
            self._subject_id = payload["sub"]
        else:
            raise SuspiciousOperation("No subject ID in token")
        return payload

    def verify_claims(self, claims):
        """Verify that userinfo claims are sufficient to allow auth"""
        # Per https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse,
        # client must validate sub in userinfo response or do nothing else with the
        # response.
        if "sub" not in claims:
            raise SuspiciousOperation("No subject ID claim")
        elif claims["sub"] != self._subject_id:
            raise SuspiciousOperation(
                'userinfo sub ("{}") does not match token sub ("{}")'.format(
                    claims["sub"], self._subject_id
                )
            )

        required_claims = {"sub", "roles"}
        if required_claims.intersection(claims.keys()) != required_claims:
            return False

        # Check datatracker roles
        claim_roles = claims["roles"]
        return ["secr", "secretariat"] in claim_roles or ["auth", "rpc"] in claim_roles
