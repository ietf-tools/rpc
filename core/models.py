# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """RPC tool user class"""
    person = models.ForeignKey(
        "DatatrackerPerson",
        null=True,
        on_delete=models.SET_NULL,
        help_text="datatracker Person linked to this user, if any",
    )


class DatatrackerPerson(models.Model):
    """Person known to the datatracker

        Relationships:
      * datatracker_subject - the datatracker subject id used to link this record to a
        datatracker Person record. This is a Person pk for now and likely forever.

      * rpc_person - the RpcPerson this User acts as. There may be multiple User accounts
        corresponding to a single RpcPerson. This will be null for a local user account.

    Merging accounts after a datatracker Person merge:
      * point the DatatrackerPerson to the correct RpcPerson
    -> the RpcPerson is really just a collection of Users to be treated as a single person.
       Classes will need to be linked to the User model, not to the RpcPerson directly.
       RFCs-to-be belonging to an RpcPerson:
         RfcToBe.objects.filter(datatracker_person__rpc_person__pk="some-pk")
    """
    datatracker_subject = models.CharField(
        max_length=255,  # per OpenID Core 1.0, 255 ASCII chars is the limit
        unique=True,
        help_text="Datatracker's subject ID for this Person",
    )
    rpc_person = models.ForeignKey("RpcPerson", null=True, on_delete=models.SET_NULL)


class RpcPerson(models.Model):
    can_hold_role = models.ManyToManyField("RpcRole")
    capable_of = models.ManyToManyField("Capability")
    hours_per_week = models.PositiveSmallIntegerField(default=40)
    manager = models.ForeignKey(
        "RpcPerson",
        null=True,
        on_delete=models.PROTECT,
        limit_choices_to={"can_hold_role__slug": "manager"},
        related_name="managed_people",
    )

    def __str__(self):
        return str(self.person)


class RpcRole(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Capability(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name
