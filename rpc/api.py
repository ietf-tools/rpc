# Copyright The IETF Trust 2023, All Rights Reserved

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

import rpcapi_client
from datatracker.rpcapi import with_rpcapi

from .models import Assignment, Cluster, Label, RfcToBe, RpcPerson
from .serializers import AssignmentSerializer, LabelSerializer, RfcToBeSerializer, RpcPersonSerializer


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


@api_view(["GET"])
def queue(request):
    """Return documents currently in the queue

    {
        "queue": [
            {
                "name" : "draft-foo-bar" #? what about April 1 things that have no draft name?
                "action_holder" : {
                    [
                        {
                            "name": "some persons name", # if there is an action holder (may evolve to a datatracker person pk)
                            "since" : "yyyy-mm-ddThh:mm:ss",  # time when was the action holder was added
                            "deadline" : "yyyy-mm-ddThh:mm:ss", # if the action holder has a deadline
                            "comment" : "whatever the comment string contained",
                        }
                        ...
                    ]
                }
                "assignments" : { # assignments that are not "done"
                    [
                        {
                            "name" : "some rpc person's name",
                            "state" : "assigned or in progress",
                        }
                        ...
                    ]
                }
                "requested_approvals" : {

                }
                "labels" :
                    [
                        { "slug": "e.g. MissRef", "color": "#FE1010"}
                    ]
            }
            ...
        ]
    }
    """
    queue = {
        "queue": [
            (
                RfcToBeSerializer(rfc_to_be).data
                | {
                    "labels": [
                        {
                            "slug": label.slug,
                            "is_exception": label.is_exception,
                        }
                        for label in rfc_to_be.labels.all()
                    ],
                    "stream": rfc_to_be.draft.stream if rfc_to_be.draft else "",
                    "deadline": rfc_to_be.external_deadline,  # todo what about internal_goal?
                    "cluster": rfc_to_be.cluster.number if rfc_to_be.cluster else None,
                    "action_holders": [
                        {
                            "name": ah.datatracker_person.plain_name(),
                            "deadline": ah.deadline,
                            "since": ah.since_when,
                            "comment": ah.comment,
                        }
                        for ah in rfc_to_be.actionholder_set.filter(
                            completed__isnull=True
                        )
                    ],
                    "assignments": [
                        {
                            "name": assignment.person.datatracker_person.plain_name(),
                            "role": assignment.role.name,
                            "state": assignment.state,
                        }
                        for assignment in rfc_to_be.assignment_set.exclude(state="done")
                    ],
                    "requested_approvals": [],
                }
            )
            for rfc_to_be in RfcToBe.objects.filter(disposition__slug="in_progress")
        ]
    }
    return JsonResponse(queue, safe=False)


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


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class RfcToBeViewSet(ModelViewSet):
    queryset = RfcToBe.objects.all()
    serializer_class = RfcToBeSerializer
    lookup_field = "draft__name"


class LabelViewSet(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
