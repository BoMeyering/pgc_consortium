"""
Data Storage Models
"""

# Standard imports
from datetime import date

# Django imports
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, validate_image_file_extension
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# External imports
from phonenumber_field.modelfields import PhoneNumberField

# App imports
from config.enumerations import AttributeDomainType, PlotType, TreatmentType, LocationType, GermplasmType, YearEnum
from config.custom_fields import KsuidField

""" Trial Models """
class Trial(models.Model):
    """
    Trial model to handle groupings of plots and phenotypes under one grouping
    FK1 on Location
    FK2 on Person
    FK3 on Organization
    """
    
    db_id = KsuidField(primary_key=True, editable=False, prefix='trial_')
    name = models.CharField(unique=True, null=False)
    location_id = models.ForeignKey(
        'resources.Location', 
        on_delete=models.CASCADE, 
        limit_choices_to={'type': 'trial'}
    )
    manager_id = models.ForeignKey('resources.Person', blank=False, null=False, on_delete=models.CASCADE)
    project_id = models.ForeignKey('resources.Project', blank=False, null=False, on_delete=models.CASCADE)
    affiliation_id = models.ForeignKey('resources.Organization', blank=False, null=False, on_delete=models.CASCADE)
    establishment_year = models.IntegerField(choices=YearEnum.choices, default=date.today().year)
    multi_year = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.name
    
class TrialYear(models.Model):
    """
    Join table for trial and year to list out all the years that a trial is planned.
    FK on Trial
    Year limited to years that are greater than or equal to the trial establishment year
    """

    db_id = KsuidField(primary_key=True, editable=False, prefix='trialYear_')
    trial_id = models.ForeignKey(Trial, on_delete=models.CASCADE, blank=False, null=False)
    year = models.IntegerField(choices=YearEnum.choices, default=date.today().year)

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
    db_id = KsuidField(primary_key=True, editable=False, prefix='trialAttr_')
    trial_id = models.ForeignKey(Trial, blank=False, null=False, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, blank=False, null=False)
    value = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

class TrialEvent(models.Model):
    """
    Trial Event model, tracks trial level agronomic processes and dates
    FK1 on Trial
    FK2 on AgroProcess
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='trialEvent_')
    trial_id = models.ForeignKey(Trial, on_delete=models.CASCADE, blank=False, null=False)
    process_id = models.ForeignKey('ontology.AgroProcess', on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    comment = models.TextField(max_length=500, blank=False, null=False)

    def __str__(self):
        return f"{self.trial_id.name} - {self.process_id.label}"
    
""" Treatment Models """
class Treatment(models.Model):
    """
    Treatment model for the main treatment group
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='treatment_')
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
    db_id = KsuidField(primary_key=True, editable=False, prefix='treatmentLevel_')
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
    db_id = KsuidField(primary_key=True, editable=False, prefix='trialTreatment_')
    trial_id = models.ForeignKey(Trial, on_delete=models.CASCADE, blank=False, null=False)
    treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trial_id', 'treatment_id'], name='trial_treatment_composite_key')
        ]

    def __str__(self):
        return f"{self.trial_id}: {self.treatment_id.name}"

""" Germplasm Models """
class CommonName(models.Model):
    """
    Common name model to hold the common name of a crop.
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='commonName_')
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Germplasm(models.Model):
    """
    Germplasm modelto hold metadata regarding a specific type pf germplasm
    FK on CommonName
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='germ_')
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
    db_id = KsuidField(primary_key=True, editable=False, prefix='germAlias_')
    germplasm_id = models.ForeignKey(Germplasm, on_delete=models.CASCADE, blank=False, null=False)
    alias = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['germplasm_id', 'alias'], name='germplasm_alias_composite_key')
        ]

    def __str__(self):
        return f"{self.alias} -> {self.germplasm_id.name}"

""" Plot Models """
class Plot(models.Model):
    """
    Plot model to handle plot objects in a trial
    FK1 on self (for nested plot structures)
    FK2 on Trial
    FK3 on Location
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='plot_')
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
        'resources.Location', 
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

    db_id = KsuidField(primary_key=True, editable=False, prefix='plotCrop_')
    plot_id = models.ForeignKey(Plot, on_delete=models.CASCADE, blank=False, null=False)
    germplasm_id = models.ForeignKey(Germplasm, on_delete=models.CASCADE, blank=False, null=False)
    plot_year = models.IntegerField(choices=YearEnum.choices, default=date.today().year)

    def clean(self):
        super().clean()

        trial = self.plot_id.trial_id

        if int(self.plot_year) < int(trial.establishment_year):
            raise ValidationError(
                {'plot_year': _(f"The plot crop year cannot be earlier than the trial establishment year ({trial.establishment_year}).")}
            )

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
    db_id = KsuidField(primary_key=True, editable=False, prefix='plotTreatment_')
    plot_crop_id = models.ForeignKey(PlotCrop, on_delete=models.CASCADE, blank=False, null=False)
    treatment_level_id = models.ForeignKey(TreatmentLevel, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.plot_crop_id.plot_id.label} - {self.plot_crop_id.plot_year}: {self.treatment_level_id.level}"

""" Observation Models """
class Observation(models.Model):
    """
    Observation model to connect observations with Person(s) PlotCrop records, and variables
    FK1 on Person
    FK2 on PlotCrop
    FK3 on Variable
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='observation_')
    date_time = models.DateTimeField(blank=False, null=False)
    observer_id = models.ForeignKey('resources.Person', on_delete=models.CASCADE, blank=False, null=False)
    plot_crop_id = models.ForeignKey(PlotCrop, on_delete=models.CASCADE, blank=False, null=False)
    variable_id = models.ForeignKey('ontology.Variable', to_field='label', on_delete=models.CASCADE)
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

