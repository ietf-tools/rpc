# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

import os

import rpcapi
from rpcapi.rest import ApiException

from django.conf import settings
from django.db import models


def get_api_client():
    """Get an RPC API client"""
    config = rpcapi.Configuration(host=settings.DATATRACKER_RPC_API_BASE)
    config.api_key["ApiKeyAuth"] = settings.DATATRACKER_RPC_API_TOKEN
    return rpcapi.ApiClient(config)


class DatatrackerPerson(models.Model):
    """Person known to the datatracker"""

    # datatracker uses AutoField for this, which is only an IntegerField, but might as well go big
    datatracker_id = models.BigIntegerField(
        unique=True, help_text="ID of the Person in the datatracker"
    )

    def __str__(self):
        return f"Datatracker Person {self.datatracker_id}"

    def plain_name(self):
        with get_api_client() as api_client:
            api_instance = rpcapi.DefaultApi(api_client)
            try:
                person = api_instance.get_person_by_id(int(self.datatracker_id))
            except ApiException as e:
                print(f"ApiException: {e}")
                person = None
        return None if person is None else person.plain_name


class Document(models.Model):
    """Document known to the datatracker"""

    # datatracker uses AutoField for this, which is only an IntegerField, but might as well go big
    datatracker_id = models.BigIntegerField(unique=True)

    # Labels applied to this instance. To track history, see
    # https://django-simple-history.readthedocs.io/en/latest/historical_model.html#tracking-many-to-many-relationships
    labels = models.ManyToManyField("rpc.Label", through="DocumentLabel")

    def __str__(self):
        return f"Doc {self.datatracker_id}"


class DocumentLabel(models.Model):
    """Through model for linking Label to Document

    This exists so we can specify on_delete=models.PROTECT for the label FK.
    """

    document = models.ForeignKey("Document", on_delete=models.CASCADE)
    label = models.ForeignKey("rpc.Label", on_delete=models.PROTECT)
