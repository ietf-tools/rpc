# Copyright The IETF Trust 2023, All Rights Reserved

import rpcapi_client

from django.conf import settings


class ApiClient(rpcapi_client.ApiClient):
    """ApiClient that obtains credentials and sets API base automatically"""

    def __init__(self):
        super().__init__(
            rpcapi_client.Configuration(
                host=settings.DATATRACKER_RPC_API_BASE,
                api_key={"ApiKeyAuth": settings.DATATRACKER_RPC_API_TOKEN}
            )
        )
