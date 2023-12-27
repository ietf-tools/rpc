# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand

from rfced.models import Index

from rpc.models import (
    RfcToBe,
    SourceFormatName,
    StdLevelName,
    StreamName,
    TlpBoilerplateChoiceName,
)


class Command(BaseCommand):
    help = "Transfer data from a dump of the current RPC production database"

    def handle(self, *args, **options):
        assert RfcToBe.objects.count() == 0
        assert StdLevelName.objects.count() == 0

        todo_std_level = StdLevelName.objects.get_or_create(
            slug="todo",
            name="Todo-stdlevel",
            desc="Don't understand std levels yet.",
        )

        todo_stream_name = StreamName.objects.get_or_create(
            slug="todo",
            name="Todo-streamname",
            desc="Don't understand streams yet",
        )

        unknown_boilerplate = TlpBoilerplateChoiceName.objects.get_or_create(
            slug="unknown",
            name="Boilerplate Unknown",
            desc="Don't know what boilerplate was used",
        )

        # TODO -  the use of these in RfcToBe may need to be m2m
        unknown_submitted_format = SourceFormatName.objects.get_or_create(
            slug="unknown",
            name="Submitted Format Unknown",
            desc="Don't know what formats were submitted",
        )

        # First get published RFCs
        for row in Index.objects.filter(type="RFC", state_id=14):
            is_apr1 = row.pub_date and row.pub_date.month == 4 and row.pub_date.day == 1
            RfcToBe.objects.create(
                disposition_id="published",
                is_april_first_rfc=True,  # should be is_apr1,
                draft=None,  # TODO
                rfc_number=int(row.doc_id[3:]),
                cluster=None,  # TODO: populate by walking Clusters table
                order_in_cluster=1,  # TODO: :point_up:
                submitted_format=unknown_submitted_format,  # TODO: verify that there's nothing currently captured
                submitted_std_level=todo_std_level,  # TODO
                submitted_boilerplate=unknown_boilerplate,  # TODO - populate those we _do_ know
                submitted_stream=todo_stream_name,  # TODO
                intended_std_level=todo_std_level,  # TODO
                intended_boilerplate=unknown_boilerplate,  # TODO
                intended_stream=todo_stream_name,  # TODO
                external_deadline=None,  # TODO - capture known ones?
                internal_goal=None,  # TODO - does the rfced db capture this?
            )
            # TODO walk states and apply labels (with history)

        # TODO
        # Get RFCs in progress
        # Get withdrawn RFCs
        # Handle other document types?
