# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

import rpcapi_client
from rpcapi_client.rest import ApiException
from datatracker.rpcapi import with_rpcapi

from django.db import models


class DatatrackerPerson(models.Model):
    """Person known to the datatracker"""

    # datatracker uses AutoField for this, which is only an IntegerField, but might as well go big
    datatracker_id = models.BigIntegerField(
        unique=True, help_text="ID of the Person in the datatracker"
    )

    def __str__(self):
        return f"Datatracker Person {self.datatracker_id}"

    @with_rpcapi
    def plain_name(self, *, rpcapi: rpcapi_client.DefaultApi):
        try:
            person = rpcapi.get_person_by_id(int(self.datatracker_id))
        except ApiException as e:
            print(f"ApiException: {e}")
            person = None
        return None if person is None else person.plain_name


class Document(models.Model):
    """Document known to the datatracker"""

    # datatracker uses AutoField for this, which is only an IntegerField, but might as well go big
    datatracker_id = models.BigIntegerField(unique=True)

    name = models.CharField(
        max_length=255, unique=True, help_text="Name of draft"
    )

    stream = models.CharField(
        max_length=32, help_text="Stream of draft"
    )
    # Labels applied to this instance. To track history, see
    # https://django-simple-history.readthedocs.io/en/latest/historical_model.html#tracking-many-to-many-relationships
    labels = models.ManyToManyField("rpc.Label", through="DocumentLabel")

    def __str__(self):
        return self.name


class DocumentLabel(models.Model):
    """Through model for linking Label to Document

    This exists so we can specify on_delete=models.PROTECT for the label FK.
    """

    document = models.ForeignKey("Document", on_delete=models.CASCADE)
    label = models.ForeignKey("rpc.Label", on_delete=models.PROTECT)
