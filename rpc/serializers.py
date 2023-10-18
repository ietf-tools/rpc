# Copyright The IETF Trust 2023, All Rights Reserved

from rest_framework import serializers

from .models import Assignment, Capability, Label, RfcToBe, RpcPerson, RpcRole


class RfcToBeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    stream = serializers.SerializerMethodField()
    pages = serializers.SerializerMethodField()

    class Meta:
        model = RfcToBe
        fields = ["id", "name", "title", "stream", "pages", "external_deadline"]

    def get_name(self, rfc_to_be):
        return rfc_to_be.draft.name

    def get_title(self, rfc_to_be):
        return rfc_to_be.draft.title

    def get_stream(self, rfc_to_be):
        return rfc_to_be.draft.stream

    def get_pages(self, rfc_to_be):
        return rfc_to_be.draft.pages


class CapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capability
        fields = ["slug", "name"]


class RpcRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcRole
        fields = ["slug", "name", "desc"]


class RpcPersonSerializer(serializers.ModelSerializer):
    """Serialize an RpcPerson

    To avoid datatracker API calls, use the `name_map` parameter to
    pass a dict mapping datatracker Person ID to name (designed for use
    with the `get_persons()` API endpoint).
    """
    name = serializers.SerializerMethodField()
    capabilities = CapabilitySerializer(source="capable_of", many=True)
    roles = RpcRoleSerializer(source="can_hold_role", many=True)

    class Meta:
        model = RpcPerson
        fields = ["id", "name", "hours_per_week", "capabilities", "roles"]

    def __init__(self, *args, **kwargs):
        self.name_map: dict[str, str] = kwargs.pop("name_map", {})  # datatracker_id -> name
        super().__init__(*args, **kwargs)

    def get_name(self, rpc_person):
        cached_name = self.name_map.get(str(rpc_person.datatracker_person.datatracker_id), None)
        return cached_name or rpc_person.datatracker_person.plain_name()


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "id",
            "rfc_to_be",
            "person",
            "role",
            "state",
            "comment",
            "time_spent",
        ]


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = [
            "slug",
            "is_exception",
            "color",
        ]
