# Copyright The IETF Trust 2023, All Rights Reserved

from rest_framework import serializers

from .models import Assignment, RfcToBe, RpcPerson, RpcRole


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
    name = serializers.SerializerMethodField()

    class Meta:
        model = RpcPerson
        fields = ["name", "can_hold_role", "capable_of"]

    def get_name(self, rpc_person):
        return rpc_person.datatracker_person.plain_name()


class RpcRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcRole
        fields = ["slug", "name", "desc"]


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

