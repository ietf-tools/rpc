# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.db import models


class DatatrackerPerson(models.Model):
    """Person known to the datatracker

      Relationships:
    * subject_id - the datatracker's OIDC subject id used to link this record to a
      datatracker Person record. This is a string representation of the Person pk for
      now and likely forever.
    """

    subject_id = models.CharField(
        max_length=255,  # per OpenID Core 1.0, 255 ASCII chars is the limit
        unique=True,
        help_text="Datatracker's subject ID for this Person",
    )

    plain_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Datatracker's plain name for this Person",
    )

    def __str__(self):
        return self.plain_name or f"Person {self.subject_id}"


class RpcPerson(models.Model):
    datatracker_person = models.ForeignKey(
        "DatatrackerPerson",
        on_delete=models.PROTECT
    )
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
        return str(self.datatracker_person)


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
