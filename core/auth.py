from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class ClaimCheckingOIDCAuthBackend(OIDCAuthenticationBackend):
    """Customized OIDC auth backend"""

    def create_user(self, claims):
        new_user = super().create_user(claims)  # sets email and username
        new_user.datatracker_subject = claims.get(
            "sub"
        )  # not permitted to be empty by OIDC Core spec
        new_user.first_name = claims.get("given_name", "")
        new_user.last_name = claims.get("family_name", "")
        new_user.save()
        return new_user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        sub = claims.get(
            "sub", None
        )  # guaranteed to exist, but might as well not fail if it is missing
        if sub is not None:
            try:
                return [self.UserModel.objects.get(datatracker_subject=sub)]
            except self.UserModel.DoesNotExist:
                pass
        return self.UserModel.objects.none()

    def verify_claims(self, claims):
        if not super().verify_claims(claims):
            return False  # basic OIDC validation failed
        # Check datatracker roles
        claim_roles = claims.get("roles", [])
        from pprint import pp
        import sys

        pp(claims)
        sys.stdout.flush()
        return ["secr", "secretariat"] in claim_roles or ["auth", "rpc"] in claim_roles
