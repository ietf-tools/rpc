# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """RPC tool user class"""
    datatracker_person = models.OneToOneField(
        "datatracker.DatatrackerPerson",
        null=True,
        on_delete=models.SET_NULL,
        help_text="Datatracker person associated with this user",
    )
