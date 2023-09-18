# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.db import models


class RpcPerson(models.Model):
    datatracker_person = models.ForeignKey(
        "datatracker.DatatrackerPerson",
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


class RfcToBe(models.Model):
    """RPC representation of a pre-publication RFC"""

    disposition = models.ForeignKey("DispositionName", on_delete=models.PROTECT)
    is_april_first_rfc = models.BooleanField(default=False)
    draft = models.ForeignKey(
        "datatracker.Document", null=True, on_delete=models.PROTECT
    )  # only null if is_april_first_rfc is True
    rfc_number = models.PositiveIntegerField(null=True)

    cluster = models.ForeignKey("Cluster", null=True, on_delete=models.SET_NULL)
    order_in_cluster = models.PositiveSmallIntegerField(default=1)

    submitted_format = models.ForeignKey("SourceFormatName", on_delete=models.PROTECT)
    submitted_std_level = models.ForeignKey(
        "StdLevelName", on_delete=models.PROTECT, related_name="+"
    )
    submitted_boilerplate = models.ForeignKey(
        "TlpBoilerplateChoiceName", on_delete=models.PROTECT, related_name="+"
    )
    submitted_stream = models.ForeignKey(
        "StreamName", on_delete=models.PROTECT, related_name="+"
    )

    intended_std_level = models.ForeignKey(
        "StdLevelName", on_delete=models.PROTECT, related_name="+"
    )
    intended_boilerplate = models.ForeignKey(
        "TlpBoilerplateChoiceName", on_delete=models.PROTECT, related_name="+"
    )
    intended_stream = models.ForeignKey(
        "StreamName", on_delete=models.PROTECT, related_name="+"
    )

    external_deadline = models.DateTimeField(null=True)
    internal_goal = models.DateTimeField(null=True)

#     history = HistoricalRecords()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(draft__isnull=False) ^ models.Q(is_april_first_rfc=True),
                name="rfctobe_draft_not_null_xor_is_april_first_rfc",
                violation_error_message="draft must be null if and only if is_april_first_rfc",
            ),
            models.UniqueConstraint(
                fields=["cluster", "order_in_cluster"],
                name="rfctobe_unique_order_in_cluster",
                violation_error_message="order in cluster must be unique",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

    def __str__(self):
        return f"RfcToBe for {self.draft if self.rfc_number is None else self.rfc_number}"


class Name(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DispositionName(Name):
    pass


class SourceFormatName(Name):
    pass


class StdLevelName(Name):
    pass


class TlpBoilerplateChoiceName(Name):
    pass


class StreamName(Name):
    pass


class Cluster(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"cluster {self.number}"


class UnusableRfcNumber(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return str(self.number)


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
