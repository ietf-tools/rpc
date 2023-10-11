# Copyright The IETF Trust 2023, All Rights Reserved

from rest_framework import serializers

from .models import Assignment, RfcToBe, RpcPerson, RpcRole


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "rfc_to_be",
            "person",
            "role",
            "state",
            "comment",
            "time_spent",
        ]


class RfcToBeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    stream = serializers.SerializerMethodField()
    pages = serializers.SerializerMethodField()

    class Meta:
        model = RfcToBe
        fields = ["id", "name", "title", "stream", "pages"]

    def get_name(self, rfc_to_be):
        return rfc_to_be.draft.name

    def get_title(self, rfc_to_be):
        return rfc_to_be.draft.title

    def get_stream(self, rfc_to_be):
        return rfc_to_be.draft.stream

    def get_pages(self, rfc_to_be):
        return rfc_to_be.draft.pages


class RpcPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcPerson
        fields = ["can_hold_role", "capable_of"]


class RpcRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcRole
        fields = ["slug", "name", "desc"]
