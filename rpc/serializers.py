# Copyright The IETF Trust 2023, All Rights Reserved

import datetime

from dataclasses import dataclass
from itertools import pairwise
from rest_framework import serializers
from simple_history.models import ModelDelta
from simple_history.utils import update_change_reason
from typing import Optional

from .models import (
    ActionHolder,
    Assignment,
    Capability,
    Label,
    RfcToBe,
    RpcPerson,
    RpcRole,
)


@dataclass
class HistoryRecord:
    id: int
    date: datetime.datetime
    by: str
    desc: str

    @classmethod
    def from_simple_history(cls, sh, desc):
        return cls(
            id=sh.id,
            date=sh.history_date,
            by=sh.history_user,
            desc=desc,
        )


class HistoryListSerializer(serializers.ListSerializer):
    def describe_model_delta(self, delta: ModelDelta):
        method = getattr(self.parent, "describe_model_delta", None) if self.parent else None
        if method is None:
            return (f"{change.field} changed from {change.old} to {change.new}" for change in delta.changes)
        return method(delta)

    def to_representation(self, data):
        records = []
        model_histories = list(data.all())
        if len(model_histories) > 0:
            for newer, older in pairwise(model_histories):
                parts = []
                if newer.history_change_reason:
                    parts.append(newer.history_change_reason)
                delta = newer.diff_against(older)
                if len(delta.changes) > 0:
                    parts.extend(self.describe_model_delta(delta))
                if len(parts) > 0:
                    records.append(HistoryRecord.from_simple_history(newer, "; ".join(parts)))
            # Always include first history
            first = model_histories[-1]
            records.append(
                HistoryRecord.from_simple_history(first, first.history_change_reason or "Record created")
            )
        return super().to_representation(records)


class HistorySerializer(serializers.Serializer):
    """Serialize the history for an RfcToBe"""
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    by = serializers.StringRelatedField()
    desc = serializers.CharField()

    class Meta:
        list_serializer_class = HistoryListSerializer


class RfcToBeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    rev = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    stream = serializers.SerializerMethodField()
    pages = serializers.SerializerMethodField()
    cluster = serializers.SerializerMethodField()
    # Need to explicitly specify labels as a PK because it uses a through model
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())
    history = HistorySerializer(many=True)

    class Meta:
        model = RfcToBe
        fields = [
            "id",
            "draft",
            "name",
            "rev",
            "title",
            "stream",
            "pages",
            "disposition",
            "external_deadline",
            "internal_goal",
            "labels",
            "cluster",
            "submitted_format",
            "submitted_boilerplate",
            "submitted_std_level",
            "submitted_stream",
            "intended_boilerplate",
            "intended_std_level",
            "intended_stream",
            "history",
        ]

    def get_name(self, rfc_to_be) -> str:
        return rfc_to_be.draft.name

    def get_rev(self, rfc_to_be) -> str:
        return rfc_to_be.draft.rev

    def get_title(self, rfc_to_be) -> str:
        return rfc_to_be.draft.title

    def get_stream(self, rfc_to_be) -> str:
        return rfc_to_be.draft.stream

    def get_pages(self, rfc_to_be) -> int:
        return rfc_to_be.draft.pages

    def get_cluster(self, rfc_to_be) -> Optional[int]:
        return rfc_to_be.cluster.number if rfc_to_be.cluster else None

    def create(self, validated_data):
        inst = super().create(validated_data)
        update_change_reason(inst, "Added to the queue")
        return inst

    def describe_model_delta(self, delta: ModelDelta):
        for change in delta.changes:
            if change.field == "labels":
                old = set(delta.old_record.labels.values_list("label__pk", flat=True))
                new = set(delta.new_record.labels.values_list("label__pk", flat=True))
                added = new - old
                removed = old - new
                changes = []
                hist_labels = Label.history.as_of(delta.new_record.history_date)
                if added:
                    added_strs = [f'"{label.slug}"' for label in hist_labels.filter(id__in=added)]
                    changes.append(
                        f"Added label{'s' if len(added_strs) > 1 else ''} {', '.join(added_strs)}"
                    )
                if removed:
                    removed_strs = [f'"{label.slug}"' for label in hist_labels.filter(id__in=removed)]
                    changes.append(
                        f"Removed label{'s' if len(removed_strs) > 1 else ''} {', '.join(removed_strs)}"
                    )
                yield " and ".join(changes)
            else:
                yield "oof"

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
        self.name_map: dict[str, str] = kwargs.pop(
            "name_map", {}
        )  # datatracker_id -> name
        super().__init__(*args, **kwargs)

    def get_name(self, rpc_person) -> str:
        cached_name = self.name_map.get(
            str(rpc_person.datatracker_person.datatracker_id), None
        )
        return cached_name or rpc_person.datatracker_person.plain_name()


class ActionHolderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ActionHolder
        fields = [
            "name",
            "deadline",
            "since_when",
            "comment",
        ]

    def get_name(self, actionholder) -> str:
        return (
            actionholder.datatracker_person.plain_name()
        )  # allow prefetched name map?


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
            "id",
            "slug",
            "is_exception",
            "color",
        ]


class QueueItemSerializer(RfcToBeSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    assignment_set = AssignmentSerializer(
        many=True, read_only=True
    )  # todo filter out "done"
    actionholder_set = ActionHolderSerializer(
        many=True, read_only=True
    )  # todo filter out "completed"
    requested_approvals = serializers.SerializerMethodField()

    class Meta(RfcToBeSerializer.Meta):
        fields = RfcToBeSerializer.Meta.fields + [
            "labels",
            "assignment_set",
            "actionholder_set",
            "requested_approvals",
        ]

    def get_requested_approvals(self, rfc_to_be) -> list:
        return []  # todo return a value
