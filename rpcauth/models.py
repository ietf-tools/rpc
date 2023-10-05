# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """RPC tool user class"""

    name = models.CharField(
        max_length=255,
        help_text="User's name",
    )

    datatracker_subject_id = models.CharField(
        max_length=255,  # per OpenID Core 1.0, 255 ASCII chars is the limit
        null=True,
        unique=True,
        help_text="Datatracker's subject ID for this User",
    )

    avatar = models.URLField(blank=True)
