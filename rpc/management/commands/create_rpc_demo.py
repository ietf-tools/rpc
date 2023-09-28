# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

import rpcapi_client
from datatracker.rpcapi import ApiClient

from ...factories import RpcPersonFactory


class Command(BaseCommand):
    help = "Populate data for RPC Tools Refresh demo"

    def handle(self, *args, **options):
        self.create_rpc_people()
        self.create_documents()

    def create_rpc_people(self):
        # From "Manage Team Members" wireframe
        with ApiClient() as api_client:
            api = rpcapi_client.client.DefaultApi(api_client)
            bjenkins = RpcPersonFactory(
                datatracker_person__datatracker_id=api.create_demo_person(
                    rpcapi_client.client.CreateDemoPersonRequest(name="B. Jenkins"),
                ).person_pk,
                can_hold_role=[
                    "formatting",
                    "first_editor",
                    "second_editor",
                    "final_review_editor",
                    "publisher",
                    "manager",
                ],
                capable_of=[
                    "codecomp-abnf",
                    "codecomp-xml",
                    "codecomp-yang",
                    "clusters-expert",
                    "ianaconsid-intermediate",
                    "xmlfmt-intermediate",
                ],
            )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="A. Travis"),
            ).person_pk,
            can_hold_role=["formatting", "first_editor", "final_review_editor"],
            capable_of=["codecomp-abnf", "clusters-beginner", "ianaconsid-beginner"],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="Chuck Brown"),
            ).person_pk,
            can_hold_role=["formatting"],
            capable_of=["clusters-beginner"],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="C. Simmons"),
            ).person_pk,
            can_hold_role=[
                "formatting",
                "first_editor",
                "second_editor",
                "final_review_editor",
            ],
            capable_of=[
                "codecomp-abnf",
                "codecomp-mib",
                "clusters-intermediate",
                "ianaconsid-beginner",
                "xmlfmt-intermediate",
            ],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="F. Fermat"),
            ).person_pk,
            can_hold_role=[
                "formatting",
                "first_editor",
                "second_editor",
                "final_review_editor",
                "publisher",
            ],
            capable_of=[
                "codecomp-yang",
                "clusters-intermediate",
                "ianaconsid-beginner",
                "xmlfmt-expert",
            ],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="K. Strawberry"),
            ).person_pk,
            can_hold_role=["formatting", "first_editor"],
            capable_of=["ianaconsid-beginner", "xmlfmt-beginner"],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="O. Bleu"),
            ).person_pk,
            can_hold_role=[
                "formatting",
                "first_editor",
                "second_editor",
                "final_review_editor",
            ],
            capable_of=[
                "codecomp-abnf",
                "codecomp-xml",
                "codecomp-yang",
                "clusters-expert",
                "ianaconsid-intermediate",
                "xmlfmt-intermediate",
            ],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="Patricia Parker"),
            ).person_pk,
            can_hold_role=[
                "formatting",
                "first_editor",
                "second_editor",
                "final_review_editor",
            ],
            capable_of=[
                "codecomp-abnf",
                "codecomp-xml",
                "codecomp-yang",
                "clusters-expert",
                "ianaconsid-expert",
                "xmlfmt-expert",
            ],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="S. Bexar"),
            ).person_pk,
            can_hold_role=[
                "formatting",
                "first_editor",
                "second_editor",
                "final_review_editor",
                "publisher",
            ],
            capable_of=[
                "codecomp-abnf",
                "codecomp-mib",
                "codecomp-xml",
                "clusters-expert",
                "ianaconsid-expert",
                "xmlfmt-expert",
            ],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="T. Langfeld"),
            ).person_pk,
            can_hold_role=["formatting", "first_editor"],
            capable_of=["ianaconsid-beginner", "xmlfmt-beginner"],
            manager=bjenkins,
        )
        RpcPersonFactory(
            datatracker_person__datatracker_id=api.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="U. Garrison"),
            ).person_pk,
            can_hold_role=["formatting"],
            capable_of=["xmlfmt-expert"],
            manager=bjenkins,
        )

    # todo bring this to life
    def create_documents(self):
        # WgDraftFactory(states=[("draft-iesg", "pub-req")])
        #
        # # Draft sent to RPC and in progress as an RfcToBe
        # RfcToBeFactory(
        #     rfc_number=None,
        #     draft__states=[("draft-iesg", "rfcqueue")]
        # )
        #
        # # Draft published as an RFC
        # rfc_number = next_rfc_number()[0]
        # RfcToBeFactory(
        #     disposition__slug="published",
        #     rfc_number=rfc_number,
        #     draft=WgRfcFactory(alias2__name=f"rfc{rfc_number}")
        # )
        pass
