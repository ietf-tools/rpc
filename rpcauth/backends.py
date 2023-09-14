# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from rpc.models import DatatrackerPerson


class RpcOIDCAuthBackend(OIDCAuthenticationBackend):
    """Customized OIDC auth backend"""

    def create_user(self, claims):
        subject_id = claims["sub"]
        # A DatatrackerPerson may exist without a user so use get_or_create()
        datatracker_person, _ = DatatrackerPerson.objects.get_or_create(
            subject_id=subject_id
        )
        try:
            # Rely on the OneToOne field to avoid creating duplicate Users for a DatatrackerPerson
            new_user = self.UserModel.objects.create(
                username=f"dt-user-{subject_id}",
                datatracker_person=datatracker_person,
            )
        except IntegrityError:
            # exception message gets logged - user only sees a failed auth
            raise SuspiciousOperation(f"User already exists for datatracker person pk={subject_id}")
        return new_user

    def filter_users_by_claims(self, claims):
        return self.UserModel.objects.filter(
            datatracker_person__subject_id__isnull=False,
            datatracker_person__subject_id=claims["sub"],  # claim guaranteed to exist
        )

    def verify_claims(self, claims):
        if not super().verify_claims(claims):
            return False  # basic OIDC validation failed
        # Check datatracker roles
        claim_roles = claims.get("roles", [])
        return ["secr", "secretariat"] in claim_roles or ["auth", "rpc"] in claim_roles
