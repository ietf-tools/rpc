from drf_spectacular.openapi import AutoSchema


class RpcAutoSchema(AutoSchema):
    # pass
    def get_tags(self):
        # Override the default so that we get a single API tag
        return ["rpc_tracker"]
