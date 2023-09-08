from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class ClaimCheckingOIDCAuthBackend(OIDCAuthenticationBackend):
  """Customized OIDC auth backend

  n.b., disregards the OIDC_USERNAME_ALGO setting used by the OIDCAuthenticationBackend
  """
  def create_user(self, claims):
    new_user = super().create_user(claims)
    new_user.first_name = claims.get("given_name", "")
    new_user.last_name = claims.get("family_name", "")
    new_user.save()
    return new_user

  def update_user(self, user, claims):
    user.first_name = claims.get("given_name", "")
    user.last_name = claims.get("family_name", "")
    user.save()
    return user
