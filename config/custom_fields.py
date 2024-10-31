"""
Custom FieldTypes
"""

from django.db import models
from charidfield import CharIDField
from ksuid import Ksuid
from functools import partial

KsuidField = partial(
    CharIDField,
    default=Ksuid,
    max_length=50,
    help_text='ksuid formatter for this entity.'
)