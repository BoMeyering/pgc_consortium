from django.contrib import admin

# Register your models here.
from .models import AttributeType, Location, State, Address, Organization, Person
from .models import Project, Trial, TrialYear, TrialAttribute
from .models import Treatment, TreatmentLevel, TrialTreatment
from .models import CommonName, Germplasm, GermplasmAlias
from .models import Plot, PlotCrop, PlotTreatment
from .models import TraitEntity, TraitAttribute, VarTrait, VarMethod, VarScale, Variable
from .models import Observation
from .models import AwsModel
from .models import Image, ImageOperation

from .filters import ManagerFilter

# Metadata Models
admin.site.register(AttributeType)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']
    ordering = ['name']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'latitude', 'longitude']
    search_fields = ['name', 'type']
    list_filter = ['type']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'address_line_1', 'city', 'state_id', 'postal_code']
    search_fields = ['name', 'address_line_1', 'address_line_2', 'building_name', 'building_suite_number', 'city', 'state_id', 'postal_code']
    list_filter = ['city', 'state_id']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation', 'ror_id', 'address_id']
    list_filter = ['address_id']
    ordering = ['name']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'affiliation_id', 'email', 'phone_number']
    search_fields = ['last_name', 'first_name', 'affiliation_id', 'email', 'phone_number', 'orcid']
    list_filter = ['affiliation_id']

# Project Level Models
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'truncate_description', 'funding', 'website']
    search_fields = ['name', 'description', 'funding']
    ordering = ['name']

@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_id', 'affiliation_id', 'manager_id', 'establishment_year', 'multi_year']
    list_filter = ['establishment_year', 'multi_year', 'affiliation_id', 'project_id', ManagerFilter]

admin.site.register(TrialYear)
admin.site.register(TrialAttribute)

# Treatment Models
@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'truncate_description']
    list_filter = ['type']
    ordering = ['name']

@admin.register(TreatmentLevel)
class TreatmentLevelAdmin(admin.ModelAdmin):
    list_display = ['treatment_id', 'level']
    list_filter = ['treatment_id']
    ordering = ['treatment_id', 'level']

@admin.register(TrialTreatment)
class TrialTreatment(admin.ModelAdmin):
    list_display = ['trial_id', 'treatment_id']
    list_filter = ['trial_id', 'treatment_id']
    ordering = ['trial_id', 'treatment_id']

# Germplasm Models
admin.site.register(CommonName)
admin.site.register(Germplasm)
admin.site.register(GermplasmAlias)

# Plot Models
admin.site.register(Plot)
admin.site.register(PlotCrop)
admin.site.register(PlotTreatment)

# Ontological Models
admin.site.register(TraitEntity)
admin.site.register(TraitAttribute)
admin.site.register(VarTrait)
admin.site.register(VarMethod)
admin.site.register(VarScale)
admin.site.register(Variable)

# Observation Models
admin.site.register(Observation)

# AWS Models
admin.site.register(AwsModel)

# Image Models
admin.site.register(Image)
admin.site.register(ImageOperation)
