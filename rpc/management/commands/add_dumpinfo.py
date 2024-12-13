# Copyright The IETF Trust 2024, All Rights Reserved
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from ...models import DumpInfo


class Command(BaseCommand):
    help = "Add DumpInfo instance with the current time"

    def handle(self, *args, **options):
        dumpinfo = DumpInfo.objects.create(timestamp=now())
        self.stdout.write(f"Set database dump timestamp to {dumpinfo.timestamp}")
