# Copyright The IETF Trust 2023, All Rights Reserved

from django.core.management.base import BaseCommand, CommandError, CommandParser

from datatracker.models import DatatrackerPerson, Document
from ...models import ActionHolder, Assignment, Cluster, Label, RfcToBe, RpcPerson


class Command(BaseCommand):
    help = "Remove all data from the database (BE CAREFUL)"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--yes-im-sure", action="store_true", dest="confirm")

    def handle(self, *args, **options):
        if not options["confirm"]:
            raise CommandError("Must confirm with '--yes-im-sure' on the command line")

        Assignment.objects.all().delete()
        ActionHolder.objects.all().delete()
        RfcToBe.objects.all().delete()
        RpcPerson.objects.all().delete()
        DatatrackerPerson.objects.all().delete()
        Document.objects.all().delete()
        Label.objects.all().delete()
        Cluster.objects.all().delete()
