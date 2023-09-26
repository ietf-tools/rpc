# Copyright The IETF Trust 2023, All Rights Reserved
# -*- coding: utf-8 -*-

import factory

from .models import (
    DatatrackerPerson,
    Document,
)


class DatatrackerPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatatrackerPerson

    datatracker_id = factory.Faker("pystr_format", string_format="######")


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    datatracker_id = factory.Faker("pyint", min_value=1, max_value=10_000_000)
