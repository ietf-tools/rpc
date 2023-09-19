# Copyright The IETF Trust 2023, All Rights Reserved

from django.http import JsonResponse

from .models import RpcPerson


def rpc_person(request):
    response = []
    for rpc_pers in RpcPerson.objects.all():
        capabilities = []
        for capability in rpc_pers.capable_of.all():
            capabilities.append(dict(id=capability.pk, name=capability.name))
        roles = []
        for role in rpc_pers.can_hold_role.all():
            roles.append(dict(id=role.pk, name=role.name))

        response.append(
            dict(
                id=rpc_pers.pk,
                name=rpc_pers.person.ascii_name(),
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
                "name": "draft-foo-bar",
                "submitted_date" : "2023-09-19",
            }
            ...
        ]
    }

    Fed by doing a server->server API query that returns essentially the union of:
    >>> Document.objects.filter(states__type_id="draft-iesg",states__slug__in=["approved","ann"])
    <QuerySet [
        <Document: draft-ietf-bess-pbb-evpn-isid-cmacflush>,
        <Document: draft-ietf-dnssd-update-lease>,
        ...
    ]>
    and
    >>> Document.objects.filter(states__type_id__in=["draft-stream-iab","draft-stream-irtf","draft-stream-ise"],states__slug__in=["rfc-edit"])
    <QuerySet [
        <Document: draft-iab-m-ten-workshop>,
        <Document: draft-irtf-cfrg-spake2>,
        ...
    ]>
    and SOMETHING ABOUT THE EDITORIAL STREAM...

    Those queries overreturn - there may be things, particularly not from the IETF stream that are already in the queue.
    This api will filter those out.
    """
    return JsonResponse({"submitted": []}, safe=False)


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
