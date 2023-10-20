# Copyright The IETF Trust 2023, All Rights Reserved

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

import rpcapi_client
from datatracker.rpcapi import with_rpcapi

from .models import Assignment, Cluster, Label, RfcToBe, RpcPerson
from .serializers import AssignmentSerializer, LabelSerializer, RfcToBeSerializer, RpcPersonSerializer


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


@api_view(["GET", "POST"])
def assignments(request):
    if request.method == "GET":
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def assignment(request, assignment_id):
    if request.method == "DELETE":
        Assignment.objects.filter(pk=assignment_id).delete()
        return Response(status=204)  # no content


@api_view(["GET"])
def rfcs_to_be(request):
    """All RfcToBe instances"""
    # only GET permitted by @api_view
    return Response(RfcToBeSerializer(RfcToBe.objects.all(), many=True).data)


@api_view(["GET"])
def rfc_to_be(request, draftname=None, rfcnum=None):
    """RfcToBe instance"""
    query = {"draft__name": draftname} if draftname else {"rfc_number": rfcnum}
    # only GET permitted by @api_view
    try:
        rfctobe = RfcToBe.objects.get(**query)
    except RfcToBe.DoesNotExist:
        return Response(status=404)
    return Response(RfcToBeSerializer(rfctobe).data)


@api_view(["GET", "PUT"])
def rfc_to_be_labels(request, draftname=None, rfcnum=None):
    """Labels on an RfcToBe"""
    query = {"draft__name": draftname} if draftname else {"rfc_number": rfcnum}
    try:
        rfctobe = RfcToBe.objects.get(**query)
    except RfcToBe.DoesNotExist:
        return Response(status=404)
    if request.method == "GET":
        return Response(LabelSerializer(rfctobe.labels.all(), many=True).data)
    elif request.method == "PUT":
        serializer = RfcToBeSerializer(rfctobe, data={"labels": request.data}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


@api_view(["GET", "POST", "PUT"])
def label(request):
    if request.method == "GET":
        return Response(LabelSerializer(Label.objects.all(), many=True).data)
    elif request.method == "POST":
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == "PUT":
        label = get_object_or_404(Label, slug=request.data["slug"])
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
