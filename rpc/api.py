# Copyright The IETF Trust 2023, All Rights Reserved

import datetime

from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import mixins, views, viewsets
from drf_spectacular.utils import extend_schema, inline_serializer

import rpcapi_client
from datatracker.rpcapi import with_rpcapi

from datatracker.models import Document
from .factories import StdLevelNameFactory, StreamNameFactory
from .models import Assignment, Cluster, Label, RfcToBe, RpcPerson, RpcRole
from .serializers import (
    AssignmentSerializer,
    LabelSerializer,
    QueueItemSerializer,
    RfcToBeSerializer,
    RpcPersonSerializer,
    RpcRoleSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def profile(request):
    """Get profile of current user"""
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"authenticated": False})
    dt_person = user.datatracker_person()
    # hasattr() test also handles None case
    rpcperson = dt_person.rpcperson if hasattr(dt_person, "rpcperson") else None
    return JsonResponse(
        {
            "authenticated": True,
            "id": user.pk,
            "name": user.name,
            "avatar": user.avatar,
            "rpcPersonId": rpcperson.id if rpcperson is not None else None,
            "isManager": (
                False
                if rpcperson is None
                else rpcperson.can_hold_role.filter(slug="manager").exists()
            ),
        }
    )


# This is for debugging / demo purposes only!
@extend_schema(operation_id="profile_retrieve_demo_only", responses=OpenApiTypes.OBJECT)
@api_view(["GET"])
def profile_as_person(request, rpc_person_id):
    rpcperson = RpcPerson.objects.filter(pk=rpc_person_id).first()
    if rpcperson is None:
        return Response(status=404)
    return JsonResponse(
        {
            "authenticated": request.user.is_authenticated,
            "id": None,
            "name": rpcperson.datatracker_person.plain_name(),
            "avatar": f"https://i.pravatar.cc/150?u={rpcperson.datatracker_person.datatracker_id}",
            "rpcPersonId": rpcperson.id,
            "isManager": (
                False
                if rpcperson is None
                else rpcperson.can_hold_role.filter(slug="manager").exists()
            ),
        }
    )

@extend_schema(responses=RpcPersonSerializer(many=True))
@api_view(["GET"])
@with_rpcapi
def rpc_person(request, *, rpcapi: rpcapi_client.DefaultApi):
    # use bulk endpoint to get names
    name_map = rpcapi.get_persons(
        list(
            RpcPerson.objects.values_list(
                "datatracker_person__datatracker_id", flat=True
            )
        )
    )
    return Response(
        RpcPersonSerializer(RpcPerson.objects.all(), many=True, name_map=name_map).data
    )


@extend_schema(
    operation_id="submissions_list", responses=OpenApiTypes.OBJECT
)  # not very specific...
@api_view(["GET"])
@with_rpcapi
def submissions(request, *, rpcapi: rpcapi_client.DefaultApi):
    """Return documents in datatracker that have been submitted to the RPC but are not yet in the queue

    {
        "submitted": [
            {
                "pk": 123456,
                "name": "draft-foo-bar",
                "stream": "ietf",
                "submitted" : "2023-09-19"
            }
            ...
        ]
    }

    Fed by doing a server->server API query that returns essentially the union of:
    >> Document.objects.filter(states__type_id="draft-iesg",states__slug__in=["approved","ann"])
    <QuerySet [
        <Document: draft-ietf-bess-pbb-evpn-isid-cmacflush>,
        <Document: draft-ietf-dnssd-update-lease>,
        ...
    ]>
    and
    >> Document.objects.filter(states__type_id__in=["draft-stream-iab","draft-stream-irtf","draft-stream-ise"],states__slug__in=["rfc-edit"])
    <QuerySet [
        <Document: draft-iab-m-ten-workshop>,
        <Document: draft-irtf-cfrg-spake2>,
        ...
    ]>
    and SOMETHING ABOUT THE EDITORIAL STREAM...

    Those queries overreturn - there may be things, particularly not from the IETF stream that are already in the queue.
    This api will filter those out.
    """
    submitted = []
    # Get submissions list from Datatracker
    response = rpcapi.submitted_to_rpc()
    submitted.extend(response.to_dict()["submitted_to_rpc"])
    # Filter out I-Ds that already have an RfcToBe
    already_in_queue = RfcToBe.objects.filter(
        draft__datatracker_id__in=[s["pk"] for s in submitted]
    ).values_list("draft__datatracker_id", flat=True)
    submitted = [s for s in submitted if s["pk"] not in already_in_queue]
    return JsonResponse({"submitted": submitted}, safe=False)


@extend_schema(operation_id="submissions_retrieve", responses=OpenApiTypes.OBJECT)
@api_view(["GET"])
@with_rpcapi
def submission(request, document_id, rpcapi: rpcapi_client.DefaultApi):
    draft = rpcapi.get_draft_by_id(document_id)
    return Response(draft.to_dict())


@extend_schema(
    operation_id="submissions_import",
    request=RfcToBeSerializer,
    responses=RfcToBeSerializer,
)
@api_view(["POST"])
@with_rpcapi
def import_submission(request, document_id, rpcapi: rpcapi_client.DefaultApi):
    """View to import a submission and create an RfcToBe"""
    # fetch and create a draft if needed
    try:
        draft = Document.objects.get(datatracker_id=document_id)
    except Document.DoesNotExist:
        draft_info = rpcapi.get_draft_by_id(document_id)
        if draft_info is None:
            return Response(status=404)
        draft, _ = Document.objects.get_or_create(
            datatracker_id=document_id,
            defaults={
                "name": draft_info.name,
                "rev": draft_info.rev,
                "title": draft_info.title,
                "stream": draft_info.stream,
                "pages": draft_info.pages,
            },
        )

    # Create the RfcToBe
    # todo get rid of the factories!
    # todo get more data from front end / think carefully about defaults
    initial_data = request.data
    initial_data.update(
        dict(
            draft=draft.pk,
            disposition="in_progress",
            submitted_boilerplate="trust200902",
            intended_boilerplate="trust200902",
            submitted_format="xml-v3",
            submitted_std_level=StdLevelNameFactory(
                slug="ps", name="Proposed Standard"
            ).pk,
            intended_std_level=StdLevelNameFactory(
                slug="ps", name="Proposed Standard"
            ).pk,
            submitted_stream=StreamNameFactory(slug="ietf", name="IETF").pk,
            intended_stream=StreamNameFactory(slug="ietf", name="IETF").pk,
            internal_goal=initial_data["external_deadline"],
        )
    )
    serializer = RfcToBeSerializer(data=initial_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)


class QueueViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # This is abusing the List action a bit - the "queue" is singular, so this
    # lists its contents. Normally we'd expect the List action to list queues and
    # the Retrieve action to retrieve a single queue. That does not apply to our
    # concept of a singular queue, so I'm using this because it works.
    queryset = RfcToBe.objects.filter(disposition__slug="in_progress")
    serializer_class = QueueItemSerializer


@api_view(["GET"])
def clusters(request):
    """Return cluster index"""
    return JsonResponse(
        [
            {
                "number": cluster.number,
                "documents": [
                    {
                        "name": rfctobe.draft.name if rfctobe.draft else None,
                        "rfc_number": rfctobe.rfc_number,
                    }
                    for rfctobe in cluster.rfctobe_set.order_by("order_in_cluster")
                ],
            }
            for cluster in Cluster.objects.all()
        ],
        safe=False,
    )


@api_view(["GET"])
def cluster(request, number):
    """Return data for a specific cluster"""
    try:
        cluster = Cluster.objects.get(number=number)
    except (Cluster.DoesNotExist, Cluster.MultipleObjectsReturned):
        return JsonResponse({"error": "Not found"}, status=404)

    return JsonResponse(
        {
            "number": cluster.number,
            "documents": [
                {
                    "name": rfctobe.draft.name if rfctobe.draft else None,
                    "rfc_number": rfctobe.rfc_number,
                }
                for rfctobe in cluster.rfctobe_set.order_by("order_in_cluster")
            ],
        }
    )


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class RfcToBeViewSet(viewsets.ModelViewSet):
    queryset = RfcToBe.objects.all()
    serializer_class = RfcToBeSerializer
    lookup_field = "draft__name"


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class RpcRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RpcRole.objects.all()
    serializer_class = RpcRoleSerializer


class StatsLabels(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="stats_labels",
        responses=inline_serializer(
            name="LabelStats",
            fields={
                "label_stats": inline_serializer(
                    name="LabelStat",
                    fields={
                        "document_id": serializers.IntegerField(),
                        "label_id": serializers.IntegerField(),
                        "seconds": serializers.FloatField(),
                    },
                    many=True,
                )
            },
        )
    )
    def get(self, request):
        results = []
        for rtb in RfcToBe.objects.all():
            for label in Label.objects.all():
                seconds_with_label = sum(
                    [
                        interval.end - interval.start
                        for interval in rtb.time_intervals_with_label(label)
                    ],
                    start=datetime.timedelta(0)
                ).total_seconds()
                if seconds_with_label > 0:
                    results.append({
                        "document_id": rtb.pk,
                        "label_id": label.pk,
                        "seconds": seconds_with_label,
                    })
        return Response({"label_stats": results})
