# Copyright The IETF Trust 2023, All Rights Reserved

from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema

import rpcapi_client
from datatracker.rpcapi import with_rpcapi

from .models import Assignment, Cluster, Label, RfcToBe, RpcPerson, RpcRole
from .serializers import (
    AssignmentSerializer,
    LabelSerializer,
    QueueItemSerializer,
    RfcToBeSerializer,
    RpcPersonSerializer,
    RpcRoleSerializer
)


@api_view(["GET"])
@with_rpcapi
def profile(request, *, rpcapi: rpcapi_client.DefaultApi):
    """Get profile of current user"""
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"authenticated": False})
    return JsonResponse({
        "authenticated": True,
        "id": user.pk,
        "name": user.name,
        "avatar": user.avatar,
    })


@extend_schema(responses=RpcPersonSerializer)
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


@extend_schema(responses=OpenApiTypes.OBJECT)  # not very specific...
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
    response = rpcapi.submitted_to_rpc()
    submitted.extend(response.to_dict()["submitted_to_rpc"])
    return JsonResponse({"submitted": submitted}, safe=False)


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
