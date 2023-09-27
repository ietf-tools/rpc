# Copyright The IETF Trust 2023, All Rights Reserved

from django.http import JsonResponse

import rpcapi
from datatracker.models import get_api_client  # todo put this somewhere real

from .models import RpcPerson


def rpc_person(request):
    response = []
    # use bulk endpoint to get names

    with get_api_client() as api_client:
        api = rpcapi.DefaultApi(api_client)
        persons = api.get_persons(
            list(
                RpcPerson.objects.values_list(
                    "datatracker_person__datatracker_id", flat=True
                )
            )
        ).persons
    name_map = dict([(p.id, p.plain_name) for p in persons])

    for rpc_pers in RpcPerson.objects.all():
        capabilities = []
        for capability in rpc_pers.capable_of.all():
            capabilities.append(dict(id=capability.pk, name=capability.name))
        roles = []
        for role in rpc_pers.can_hold_role.all():
            roles.append(dict(id=role.pk, name=role.name))
        # Look up the name, but allow for the slim possibility an RpcPerson was created between
        # when we looked up the name_map and when we started this loop.
        name = name_map.get(rpc_pers.datatracker_person.datatracker_id, None)
        response.append(
            dict(
                id=rpc_pers.pk,
                name=name or rpc_pers.datatracker_person.plain_name(),
                capabilities=capabilities,
                roles=roles,
            )
        )

    return JsonResponse(response, safe=False)


def submissions(request):
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
    with get_api_client() as api_client:
        api = rpcapi.DefaultApi(api_client)
        response = api.submitted_to_rpc()
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
                            "deadline" : "yyyy-mm-dd", # if the action holder has a deadline
                            "comment" : "whatever the comment string contained",
                            "by" : "some rpc person's name", # May evolve to be a rpcperson_pk
                            "time" : "time of the comment"
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
    return JsonResponse({"queue": []}, safe=False)
