# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

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
            raise SuspiciousOperation(f"User already exists for datatracker person pk={subject_id}")
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

    def verify_claims(self, claims):
        """Verify that claims are sufficient to allow auth"""
        required_claims = {"sub", "roles"}
        if required_claims.intersection(claims.keys()) != required_claims:
            return False

        # Per https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse, must validate sub in userinfo
        # response
        if claims["sub"] != self.OIDC_RP_CLIENT_ID:
            raise SuspiciousOperation("userinfo sub does not match client ID")

        # Check datatracker roles
        claim_roles = claims["roles"]
        return ["secr", "secretariat"] in claim_roles or ["auth", "rpc"] in claim_roles
