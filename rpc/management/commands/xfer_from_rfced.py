# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

import rpcapi_client

from django.core.management.base import BaseCommand

from datatracker.models import Document
from datatracker.rpcapi import with_rpcapi

from rfced.models import Index

from ...models import (
    RfcToBe,
    SourceFormatName,
    StdLevelName,
    StreamName,
    TlpBoilerplateChoiceName,
)


@with_rpcapi
def update_documents(docnames, *, rpcapi: rpcapi_client.DefaultApi):
    documents = rpcapi.get_drafts_by_names(docnames)
    for name in docnames:
        if name not in documents:
            print(f"skipping create_or_update of {name}")
            continue
        docinfo = documents[name]
        doc, created = Document.objects.get_or_create(
            datatracker_id=docinfo["id"],
            defaults={
                "name": docinfo["name"],
                "rev": docinfo["rev"],
                "title": docinfo["title"],
                "stream": docinfo["stream"],
                "pages": docinfo["pages"],
            },
        )
        if not created:
            # Update the record with latest information
            assert doc.name == docinfo["name"]
            doc.rev = docinfo["rev"]
            doc.title = docinfo["title"]
            doc.stream = docinfo["stream"]
            doc.pages = docinfo["pages"]
            doc.save()

        # TODO: not doing anything with authors...


class Command(BaseCommand):
    help = "Transfer data from a dump of the current RPC production database"

    def handle(self, *args, **options):
        assert RfcToBe.objects.count() == 0

        self.todo_std_level, _ = StdLevelName.objects.get_or_create(
            slug="todo",
            name="Todo-stdlevel",
            desc="Don't understand std levels yet.",
        )

        self.todo_stream_name, _ = StreamName.objects.get_or_create(
            slug="todo",
            name="Todo-streamname",
            desc="Don't understand streams yet",
        )

        self.unknown_boilerplate, _ = TlpBoilerplateChoiceName.objects.get_or_create(
            slug="unknown",
            name="Boilerplate Unknown",
            desc="Don't know what boilerplate was used",
        )

        self.unknown_submitted_format, _ = SourceFormatName.objects.get_or_create(
            slug="unknown",
            name="Submitted Format Unknown",
            desc="Don't know what formats were submitted",
        )

        self.get_published_rfcs()

        # TODO
        # Get RFCs in progress
        # Get withdrawn RFCs
        # Handle other document types (?)
        #   >>> Counter(Index.objects.values_list('type',flat=True))
        #   Counter({'RFC': 9775, 'IEN': 208, 'BCP': 31, 'STD': 27})

    def get_published_rfcs(self):
        rfc_qs = Index.objects.filter(type="RFC", state_id=14).exclude(
            status="NOT ISSUED"
        )
        names = (
            rfc_qs.exclude(draft__isnull=True)
            .exclude(draft="")
            .exclude(pub_date__month=4, pub_date__day=1)
            .exclude(
                doc_id__in=["RFC2605", "RFC3018", "RFC6019", "RFC6342", "RFC7159"]
            )  # anomalous draft values
            .values_list("draft", flat=True)
        )
        # All remaining draft names include version numbers - strip them
        update_documents([name.strip()[:-3] for name in names])

        # First get published RFCs
        problematic = []
        nodraft = []
        for row in Index.objects.filter(type="RFC", state_id=14).exclude(
            status="NOT ISSUED"
        ):
            is_apr1 = (
                row.pub_date and row.pub_date.month == 4 and row.pub_date.day == 1
            ) or False
            found_doc = None
            if not is_apr1:
                if row.draft is None or row.draft == "":
                    nodraft.append(row.doc_id)

                    continue  # TODO solve the problem
                # These are anomolies in the incoming data
                # Some are missing drafts, some are republications of RFCs because of errors
                # ('RFC3018', 'draft-bogdanov-umsp')
                # ('RFC2605', 'draft-ietf-madman-dsa-mib-1')
                # ('RFC6019', 'rfc4049bis')
                # ('RFC6342', 'draft-ietf-v6ops-v6-in-mobile-networks-rfc6312bis')
                # ('RFC7159', 'draft-ietf-json-rfc4627bis-rfc7159bis')
                if row.doc_id in [
                    "RFC2605",
                    "RFC3018",
                    "RFC6019",
                    "RFC6342",
                    "RFC7159",
                ]:
                    problematic.append(row.doc_id)
                    continue  # TODO solve the problem
                found_doc = Document.objects.filter(name=row.draft.strip()[:-3]).first()
                if not found_doc:
                    print(f"Skipping {row.doc_id} - problem with {row.draft}")
                    continue
            RfcToBe.objects.create(
                disposition_id="published",
                is_april_first_rfc=is_apr1,
                draft=found_doc if not is_apr1 else None,
                rfc_number=int(row.doc_id[3:]),
                cluster=None,  # TODO: populate by walking Clusters table
                order_in_cluster=1,  # TODO: :point_up:
                submitted_format=self.unknown_submitted_format,  # TODO: verify that there's nothing currently captured
                submitted_std_level=self.todo_std_level,  # TODO
                submitted_boilerplate=self.unknown_boilerplate,  # TODO - populate those we _do_ know
                submitted_stream=self.todo_stream_name,  # TODO
                intended_std_level=self.todo_std_level,  # TODO
                intended_boilerplate=self.unknown_boilerplate,  # TODO
                intended_stream=self.todo_stream_name,  # TODO
                external_deadline=None,  # TODO - capture known ones?
                internal_goal=None,  # TODO - does the rfced db capture this?
            )
            # TODO walk states and apply labels (with history)

        print(
            "Skipped the following as they had no draft names populated (model breaks)"
        )
        print(sorted(nodraft))
        print("")
        print("Skipped the following known problematic drafts")
        print(sorted(problematic))
