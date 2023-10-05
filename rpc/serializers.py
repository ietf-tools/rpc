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
    class Meta:
        model = RfcToBe
        fields = ["id"]


class RpcPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcPerson
        fields = ["can_hold_role", "capable_of"]


class RpcRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcRole
        fields = ["slug", "name", "desc"]
