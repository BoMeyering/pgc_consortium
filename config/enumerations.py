"""
Enumerations and FieldTypes
"""

from django.db import models
from ksuid import Ksuid
from functools import partial
from datetime import date, datetime
from enum import IntEnum, Enum

""" Enumerations """    
class VariableType(models.TextChoices):
    """
    Enumerate the different variable types
    """
    CORN = 'corn', 'Corn'
    SOYBEAN = 'soybean', 'Soybean'
    PGC_GRASS = 'pgc grass', 'PGC Grass'
    PGC_CLOVER = 'pgc clover', 'PGC Clover'
    WEED = 'weed', 'Weed'
    SOIL = 'soil', 'Soil'
    
class StatusType(models.TextChoices):
    """
    Enumerate all status types
    """
    SUCCESS = 'success', 'Success'
    IN_PROGRESS = 'in progress', 'In Progress'
    FAILURE = 'failure', 'Failure'
    
class AttributeDomainType(models.TextChoices):
    """
    Enumerate all the things!
    """
    TRIAL = 'trial', 'Trial'
    PROJECT = 'project', 'Project'
    GERMPLASM = 'germplasm', 'Germplasm'
    
class PlotType(models.TextChoices):
    """
    Enumerate all plot types
    """
    MAIN_PLOT = 'main plot', 'Main Plot'
    SPLIT_PLOT = 'split plot', 'Split Plot'
    SPLIT_SPLIT_PLOT = 'split split plot', 'Split Split Plot'
    SPLIT_SPLIT_SPLIT_PLOT = 'split split split plot', 'Split Split Split Plot'
    
class TreatmentType(models.TextChoices):
    """
    Enumerate all of the treatment group types
    """
    GERMPLASM = 'germplasm', 'Germplasm'        # planting different germplasm
    PLANTING = 'planting', 'Planting'           # row spacing, seeding rates, etc.
    FERTILIZER = 'fertilizer', 'Fertilizer'     # different fertilizers, rates, etc.
    OPERATIONS = 'operations', 'Operations'     # Harvest schedules, residue treatments, etc.
    HERBICIDE = 'herbicide', 'Herbicide'        # different herbicides, rates, etc.
    OTHER = 'other', 'Other'                    # Everything else.

class LocationType(models.TextChoices):
    """
    Enumeration for all location types
    """
    PLOT = 'plot', 'Plot'
    TRIAL = 'trial', 'Trial'
    GENERAL = 'general', 'General'

class GermplasmType(models.TextChoices):
    """
    Enumerate all of the germplasm types
    """
    PGC = 'pgc', 'PGC'
    CROP = 'crop', 'Crop'

class YearEnum(Enum):
    """
    Enumerate all the year choices
    """
    @classmethod
    def choices(cls):
        current_year = date.today().year
        print(datetime.now())
        return [(year, str(year)) for year in range(1970, current_year + 20)]