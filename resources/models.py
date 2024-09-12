"""
Resource Level Models
"""
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

# External imports
from phonenumber_field.modelfields import PhoneNumberField

# App imports
from config.enumerations import AttributeDomainType, LocationType
from config.custom_fields import KsuidField

""" Resource Models """
class Attribute(models.Model):
    """
    REVAMP THIS MODEL AND REVISIT LATER
    Miscellaneous attribute model
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='attr_')
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
    db_id = KsuidField(primary_key=True, editable=False, prefix='loc_')
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
    db_id = KsuidField(primary_key=True, editable=False, prefix='state_')
    name = models.CharField(max_length=255, null=False, unique=True)
    abbreviation = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f"{self.name}, {self.abbreviation}"

class Address(models.Model):
    """
    Address to handle address objects for organizations
    FK on State
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='addr_')
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
    db_id = KsuidField(primary_key=True, editable=False, prefix='org_')
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
    logo_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Person(models.Model):
    """
    Person model
    FK on Organization
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='person_')
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    middle_initial = models.CharField(max_length=1)
    affiliation_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    orcid = models.CharField(max_length=19, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=False)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.affiliation_id}"

class Project(models.Model):
    """
    Project model to handle trial groupings into a project
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='proj_')
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
