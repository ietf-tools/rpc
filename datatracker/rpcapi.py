# Copyright The IETF Trust 2023, All Rights Reserved

from functools import wraps
import rpcapi_client

from django.conf import settings


class ApiClient(rpcapi_client.ApiClient):
    """ApiClient that obtains credentials and sets API base automatically"""

    def __init__(self):
        super().__init__(
            rpcapi_client.Configuration(
                host=settings.DATATRACKER_RPC_API_BASE,
                api_key={"ApiKeyAuth": settings.DATATRACKER_RPC_API_TOKEN},
            )
        )


def with_rpcapi(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "rpcapi" in kwargs:
            # Let an api instance be passed through
            return f(*args, **kwargs)

        # Create our own api instance and pass it to the wrapped function
        with ApiClient() as client:
            kwargs["rpcapi"] = rpcapi_client.DefaultApi(client)
            return f(*args, **kwargs)

    return wrapper
