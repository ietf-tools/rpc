# Copyright The IETF Trust 2024, All Rights Reserved
"""Production-mode Django settings for RPC project"""
from .base import *

def _multiline_to_list(s):
    """Helper to split at newlines and convert to list"""
    return [item.strip() for item in s.split("\n") if item.strip()]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["PURPLE_DJANGO_SECRET_KEY"]
assert not SECRET_KEY.startswith(
    "django-insecure"
)  # be sure we didn't get the dev secret

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = _multiline_to_list(os.environ["PURPLE_ALLOWED_HOSTS"])

# Datatracker config
#
# For real production use, should not need to configure any of the env vars
# except PURPLE_RPC_API_TOKEN.
DATATRACKER_RPC_API_TOKEN = os.environ["PURPLE_RPC_API_TOKEN"]
DATATRACKER_BASE = os.environ.get(
    "PURPLE_DATATRACKER_BASE", "https://datatracker.ietf.org"
)
DATATRACKER_RPC_API_BASE = os.environ.get(
    "PURPLE_DATATRACKER_RPC_API_BASE", f"{DATATRACKER_BASE}/api/rpc"
)
DATATRACKER_API_V1_BASE = os.environ.get(
    "PURPLE_DATATRACKER_API_V1_BASE", f"{DATATRACKER_BASE}/api/v1"
)


# OIDC configuration (see also base.py)
OIDC_OP_ISSUER_ID = os.environ.get(
    "PURPLE_OIDC_OP_ISSUER_ID", f"{DATATRACKER_BASE}/api/openid"
)
OIDC_OP_JWKS_ENDPOINT = os.environ.get(
    "PURPLE_OIDC_OP_JWKS_ENDPOINT", f"{OIDC_OP_ISSUER_ID}/jwks/"
)
OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ.get(
    "PURPLE_OIDC_OP_AUTHORIZATION_ENDPOINT", f"{OIDC_OP_ISSUER_ID}/authorize/"
)
OIDC_OP_TOKEN_ENDPOINT = os.environ.get(
    "PURPLE_OIDC_OP_TOKEN_ENDPOINT", f"{OIDC_OP_ISSUER_ID}/token/"
)
OIDC_OP_USER_ENDPOINT = os.environ.get(
    "PURPLE_OIDC_OP_USER_ENDPOINT", f"{OIDC_OP_ISSUER_ID}/userinfo/"
)
