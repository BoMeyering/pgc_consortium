
import uuid
from ksuid import Ksuid
import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, validate_image_file_extension
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


from datetime import date

from phonenumber_field.modelfields import PhoneNumberField
from enum import Enum


""" ID Functions """
def generate_ksuid():
    """
    Generate a K-Sorted Universal ID
    """
    return str(Ksuid())

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

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]
    
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

""" Metadata Models"""
class AttributeType(models.Model):
    """
    REVAMP THIS MODEL AND REVISIT LATER
    Miscellaneous attribute model
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(null=False, blank=False)
    abbreviation = models.CharField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    domain = models.CharField(
        max_length=50,
        choices = AttributeDomainType,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"{self.label} - {self.domain}"

class Location(models.Model):
    """
    Location model for plots, trial, and general locations
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(null=False, choices=LocationType)

    def get_absolute_url(self):
        return reverse(
            'data_storage:show_location',
            args=[self.db_id]
        )

    def __str__(self):
        return f"{self.name} - {self.latitude, self.longitude}"

class State(models.Model):
    """
    State model to be populated with all 50 US states
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    abbreviation = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f"{self.name}, {self.abbreviation}"

class Address(models.Model):
    """
    Address to handle address objects for organizations
    FK on State
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    address_line_1 = models.CharField(max_length=255, blank=False, null=False)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=50, blank=True, null=True)
    building_suite_number = models.CharField(max_length=50, blank=True, null=True)  # Optional field for building or suite number
    city = models.CharField(max_length=100)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    postal_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{5}(?:-\d{4})?$',
                message="Enter a valid US postal code in the format XXXXX or XXXXX-XXXX."
            ),
        ]
    )

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state_id.name} {self.postal_code}"

class Organization(models.Model):
    """
    Organization model for different research institutions, companies, and groups
    FK on Address
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(blank=False, null=False, unique=True)
    abbreviation = models.CharField(blank=False, null=False, unique=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=False)
    ror_id = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^https://ror\.org/[a-zA-Z0-9]{9}$',
                message="Enter a valid ROR ID in the format https://ror.org/XXXXXXXXX."
            ),
        ],
        unique=True
    )

    def __str__(self):
        return self.name
    
class Person(models.Model):
    """
    Person model
    FK on Organization
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    middle_initial = models.CharField(max_length=1)
    affiliation_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    orcid = models.CharField(max_length=19, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=False)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.affiliation_id}"

""" Project Level Models"""
class Project(models.Model):
    """
    Project model to handle trial groupings into a project
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(unique=True, null=False)
    description = models.TextField(blank=False, null=False)
    funding = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    def truncate_description(self):
        """Return a truncated description for displaying in the admin page"""
        if len(self.description) > 50:
            return format_html('{}...', self.description[:50])
        return self.description
    
    def __str__(self):
        return self.name

class Trial(models.Model):
    """
    Trial model to handle groupings of plots and phenotypes under one grouping
    FK1 on Location
    FK2 on Person
    FK3 on Organization
    """
    YEAR_CHOICES = [(r, str(r)) for r in range(1970, date.today().year + 1)]
    
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(unique=True, null=False)
    location_id = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        limit_choices_to={'type': 'trial'}
    )
    manager_id = models.ForeignKey(Person, blank=False, null=False, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, blank=False, null=False, on_delete=models.CASCADE)
    affiliation_id = models.ForeignKey(Organization, blank=False, null=False, on_delete=models.CASCADE)
    establishment_year = models.CharField(max_length=4, choices=YEAR_CHOICES, default=date.today().year)
    multi_year = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.name
    
class TrialYear(models.Model):
    """
    Join table for trial and year to list out all the years that a trial is planned.
    FK on Trial
    Year limited to years that are greater than or equal to the trial establishment year
    """
    YEAR_CHOICES = [(r, str(r)) for r in range(1900, date.today().year + 1)]

    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    trial_id = models.ForeignKey(Trial, on_delete=models.CASCADE, blank=False, null=False)
    year = models.IntegerField(choices=YEAR_CHOICES, default=date.today().year)

    def clean(self):
        super().clean()

        trial = self.trial_id

        if int(self.year) < int(trial.establishment_year):
            raise ValidationError(
                {'year': _(f"The trial year cannot be earlier than the trial establishment year ({trial.establishment_year}).")}
            )
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trial_id', 'year'], name='trial_year_composite_key')
        ]
    
    def __str__(self):
        return f"{self.trial_id.name} - {self.year}"

class TrialAttribute(models.Model):
    """
    Trial Attribute model
    FK on Trial
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    trial_id = models.ForeignKey(Trial, blank=False, null=False, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, blank=False, null=False)
    value = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f"{self.key}: {self.value}"

""" Treatment Models """
class Treatment(models.Model):
    """
    Treatment model for the main treatment group
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    type = models.CharField(max_length=255, choices=TreatmentType)
    description = models.TextField(max_length=500, blank=False, null=False)

    def truncate_description(self):
        """Return a truncated description for displaying in the admin page"""
        if len(self.description) > 50:
            return format_html('{}...', self.description[:50])
        return self.description
    
    def __str__(self):
        return f"{self.name} ({self.type})"

class TreatmentLevel(models.Model):
    """
    Treatment Level model for set factors of a given treatment
    FK on Treatment
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    level = models.CharField(max_length=255, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['treatment_id', 'level'], name='treatment_level_composite_key')
        ]

    def __str__(self):
        return f"{self.treatment_id.name}: {self.level}"
    
class TrialTreatment(models.Model):
    """
    Trial Treatment join table to connect trials with treatment groups
    FK1 on Trial
    FK2 on Treatment
    Composite key constraint on Trial and Treatment
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    trial_id = models.ForeignKey(Trial, on_delete=models.CASCADE, blank=False, null=False)
    treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trial_id', 'treatment_id'], name='trial_treatment_composite_key')
        ]

    def __str__(self):
        return f"{self.trial_id}: {self.treatment_id.name}"

""" Germplasm """
class CommonName(models.Model):
    """
    Common name model to hold the common name of a crop.
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Germplasm(models.Model):
    """
    Germplasm modelto hold metadata regarding a specific type pf germplasm
    FK on CommonName
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    type = models.CharField(max_length=255, choices=GermplasmType)
    common_name_id = models.ForeignKey(CommonName, on_delete=models.SET_NULL, null=True, blank=False)
    genus = models.CharField(max_length=255, blank=False, null=False)
    species = models.CharField(max_length=255, blank=False, default='spp.')

    def __str__(self):
        return f"{self.type} {self.common_name_id} - {self.name}"

class GermplasmAlias(models.Model):
    """
    Germplasm Alias model to handle other germplasm names that might appear
    FK on Germplasm
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    germplasm_id = models.ForeignKey(Germplasm, on_delete=models.CASCADE, blank=False, null=False)
    alias = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['germplasm_id', 'alias'], name='germplasm_alias_composite_key')
        ]

    def __str__(self):
        return f"{self.alias} -> {self.germplasm_id.name}"

""" Plots """
class Plot(models.Model):
    """
    Plot model to handle plot objects in a trial
    FK1 on self (for nested plot structures)
    FK2 on Trial
    FK3 on Location
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    trial_id = models.ForeignKey(
        Trial, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False, 
        related_name='plots'
    )
    label = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(choices=PlotType, blank=False, null=False)
    block = models.CharField(max_length=50, blank=True, null=True)
    row = models.CharField(max_length=10, blank=True, null=True)
    column = models.CharField(max_length=10, blank=True, null=True)
    width_m = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        help_text='The width of the plot object in meters.'
    )
    length_m = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        help_text='The length of the plot object in meters.'
    )
    parent_plot_id = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    location_id = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        limit_choices_to={'type': 'plot'},
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trial_id', 'label'], name='plot_trial_unique_constraint')
        ]

    def __str__(self):
        return f"{self.trial_id.name} - {self.label} "
    
class PlotCrop(models.Model):
    """
    Plot Crop join table
    FK1 on Plot
    FK2 on Germplasm
    Composite key unique constraint on plot_id, germplasm_id, and year
    """
    YEAR_CHOICES = [(r, str(r)) for r in range(1900, date.today().year + 1)]

    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    plot_id = models.ForeignKey(Plot, on_delete=models.CASCADE, blank=False, null=False)
    germplasm_id = models.ForeignKey(Germplasm, on_delete=models.CASCADE, blank=False, null=False)
    plot_year = models.CharField(max_length=4, choices=YEAR_CHOICES, default=date.today().year)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['plot_id', 'germplasm_id', 'plot_year'], name='plot_crop_composite_key')
        ]

    def __str__(self):
        return f"{self.plot_id.label} - {self.plot_year} - {self.germplasm_id.name}"

class PlotTreatment(models.Model):
    """
    Plot Treatment join table
    FK1 on Plot
    FK2 on TreatmentLevel
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    plot_crop_id = models.ForeignKey(PlotCrop, on_delete=models.CASCADE, blank=False, null=False)
    treatment_level_id = models.ForeignKey(TreatmentLevel, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.plot_crop_id.plot_id.label} - {self.plot_crop_id.plot_year}: {self.treatment_level_id.level}"

""" Ontological Terms """
class TraitEntity(models.Model):
    """
    Entity model holds the label information about a specific trait entity object
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class TraitAttribute(models.Model):
    """
    Attribute model holds the label information about a specific trait attribute object
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class VarTrait(models.Model):
    """
    Trait model holds the specific trait identity for a given variable.
    FK on TraitEntity
    FK on TraitAttrribute
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    entity_id = models.ForeignKey(TraitEntity, on_delete=models.CASCADE, blank=False, null=False)
    attribute_id = models.ForeignKey(TraitAttribute, on_delete=models.CASCADE, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class VarMethod(models.Model):
    """
    Method model holds variable method label and descriptions
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class VarScale(models.Model):
    """
    Scale model holds variable scale label and descriptions
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class Variable(models.Model):
    """
    Variable model for the ontology
    FK1 on VarTrait
    Fk2 on VarMethod
    FK3 on VarScale
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    abbreviation = models.CharField(max_length=255, unique=True, blank=False, null=False)
    trait_id = models.ForeignKey(VarTrait, on_delete=models.CASCADE, blank=False, null=False)
    method_id = models.ForeignKey(VarMethod, on_delete=models.CASCADE, blank=False, null=False)
    scale_id = models.ForeignKey(VarScale, on_delete=models.CASCADE, blank=False, null=False)
    sop_url = models.URLField(blank=True, null=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=VariableType, blank=False, null=False)
    
    def __str__(self):
        return f"{self.label} - ({self.abbreviation})"

""" Observation Tables """
class Observation(models.Model):
    """
    Observation model to connect observations with Person(s) PlotCrop records, and variables
    FK1 on Person
    FK2 on PlotCrop
    FK3 on Variable
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    date_time = models.DateTimeField(blank=False, null=False)
    observer_id = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)
    plot_crop_id = models.ForeignKey(PlotCrop, on_delete=models.CASCADE, blank=False, null=False)
    variable_id = models.ForeignKey(Variable, to_field='label', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, null=False)

    def clean(self):
        super().clean()

        variable = self.variable_id

        if variable.min_value:
            if self.value < variable.min_value:
                raise ValidationError(
                    {'value': _(f"The observation value cannot be less than the variable {variable}'s minimum allowed value ({variable.min_value})")}
                )
        if variable.max_value:
            if self.value > variable.max_value:
                raise ValidationError(
                    {'value': _(f"The observation value cannot be less than the variable {variable}'s maximum allowed value ({variable.max_value})")}
                )

    def __str__(self):
        return f"{self.plotId} - {self.variable}: {self.value}"

""" AWS Models """
class AwsModel(models.Model):
    """
    AWS Model structure to record all different AWS models in the system
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    version = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    endpoint_url = models.URLField(null=False, blank=False)

    def __str__(self):
        return f"{self.name} - {self.version}"

""" Image and File Storage """
class Image(models.Model):
    """
    Image model for determining the structure of images connected to a specific observation
    FK on Observation
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    filename = models.CharField(
        max_length=255, 
        blank=False, 
        null=False, 
        validators=[
            validate_image_file_extension
        ]
    )
    height = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99999)
        ]
    )
    width = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99999)
        ]
    )
    creation_date_time = models.DateTimeField(blank=False, null=False)
    storage_url = models.URLField(blank=False, null=False)
    observation_id = models.ForeignKey(Observation, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        if self.observation_id:
            observation = self.observation_id
            return f"{self.filename} - {self.creation_date_time} - {self.observation_id.variable_id.label}"
        else:
            return f"{self.filename} - {self.creation_date_time} - No observations linked"

class ImageOperation(models.Model):
    """
    Image Operation model outlines the structure of individual operations performed on an image by a model
    FK1 on Image
    FK2 on AwsModel
    """
    db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False, null=False)
    model_id = models.ForeignKey(AwsModel, on_delete=models.CASCADE, blank=False, null=False)
    date_time = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    status = models.CharField(max_length=50, choices=StatusType)

    def __str__(self):
        return f"{self.image_id} - {self.model_id} - {self.date_time}: {self.status}"
 