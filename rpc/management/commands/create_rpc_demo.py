# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

import datetime

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

import rpcapi_client
from datatracker.rpcapi import with_rpcapi

from ...factories import RfcToBeFactory, RpcPersonFactory
from ...models import RpcPerson


class Command(BaseCommand):
    help = "Populate data for RPC Tools Refresh demo"

    def handle(self, *args, **options):
        self.people: dict[str, RpcPerson] = {}
        self.create_rpc_people()
        self.create_documents()

    @with_rpcapi
    def create_rpc_people(self, *, rpcapi: rpcapi_client.DefaultApi):
        # From "Manage Team Members" wireframe

        self.people["bjenkins"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="B. Jenkins"),
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
        self.people["atravis"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="A. Travis"),
            ).person_pk,
            can_hold_role=["formatting", "first_editor", "final_review_editor"],
            capable_of=["codecomp-abnf", "clusters-beginner", "ianaconsid-beginner"],
            manager=self.people["bjenkins"],
        )
        self.people["cbrown"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="Chuck Brown"),
            ).person_pk,
            can_hold_role=["formatting"],
            capable_of=["clusters-beginner"],
            manager=self.people["bjenkins"],
        )
        self.people["csimmons"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
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
            manager=self.people["bjenkins"],
        )
        self.people["ffermat"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
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
            manager=self.people["bjenkins"],
        )
        self.people["kstrawberry"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="K. Strawberry"),
            ).person_pk,
            can_hold_role=["formatting", "first_editor"],
            capable_of=["ianaconsid-beginner", "xmlfmt-beginner"],
            manager=self.people["bjenkins"],
        )
        self.people["obleu"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
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
            manager=self.people["bjenkins"],
        )
        self.people["pparker"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
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
            manager=self.people["bjenkins"],
        )
        self.people["sbexar"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
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
            manager=self.people["bjenkins"],
        )
        self.people["tlangfeld"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="T. Langfeld"),
            ).person_pk,
            can_hold_role=["formatting", "first_editor"],
            capable_of=["ianaconsid-beginner", "xmlfmt-beginner"],
            manager=self.people["bjenkins"],
        )
        self.people["ugarrison"] = RpcPersonFactory(
            datatracker_person__datatracker_id=rpcapi.create_demo_person(
                rpcapi_client.CreateDemoPersonRequest(name="U. Garrison"),
            ).person_pk,
            can_hold_role=["formatting"],
            capable_of=["xmlfmt-expert"],
            manager=self.people["bjenkins"],
        )

    @with_rpcapi
    def create_documents(self, *, rpcapi: rpcapi_client.DefaultApi):
        rpcapi.create_demo_draft(
            rpcapi_client.CreateDemoDraftRequest(
                name="draft-ietf-foo-pubreq-00",
                states=[("draft-iesg", "pub-req")],
            )
        )

        # Draft sent to RPC and in progress as an RfcToBe
        self._demo_rfctobe_factory(
            rpcapi=rpcapi,
            name="draft-ietf-tasty-cheese-00",
            states=[("draft-iesg", "rfcqueue")],
        )

        self._demo_rfctobe_factory(
            rpcapi=rpcapi,
            name="draft-ietf-where-is-my-hat-00",
            states=[("draft-iesg", "rfcqueue")],
            external_deadline=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=30),
        )

        self._demo_rfctobe_factory(
            rpcapi=rpcapi,
            name="draft-irtf-improving-lizard-qol-00",
            stream="irtf",
            states=[("draft-iesg", "idexists")],
        )
        #
        # # Draft published as an RFC
        # rfc_number = next_rfc_number()[0]
        # RfcToBeFactory(
        #     disposition__slug="published",
        #     rfc_number=rfc_number,
        #     draft=WgRfcFactory(alias2__name=f"rfc{rfc_number}")
        # )

    @with_rpcapi
    def _demo_rfctobe_factory(
        self,
        *,
        rpcapi: rpcapi_client.DefaultApi,
        name,
        states=None,
        stream="ietf",
        **kwargs,
    ):
        """Create a document on the back end and generate an RfcToBe linked to it

        **kwargs are passed through to the RfcToBeFactory
        """
        dtdoc = rpcapi.create_demo_draft(
            rpcapi_client.CreateDemoDraftRequest(
                name=name, states=states, stream=stream
            )
        )
        try:
            RfcToBeFactory(
                **kwargs,
                draft__pk=dtdoc.doc_id,
                draft__name=dtdoc.name,
            )
        except IntegrityError:
            print(
                f">>> Warning: Failed to create RfcToBe for {dtdoc.name}, already exists?"
            )

