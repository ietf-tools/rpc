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
