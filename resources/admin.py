from django.contrib import admin
from .models import Attribute, Location, State, Address, Organization, Person, Project

# Register your models here.
admin.site.register(Attribute)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'latitude', 'longitude']
    search_fields = ['name', 'type']
    list_filter = ['type']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']
    ordering = ['name']

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

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'truncate_description', 'funding', 'website']
    search_fields = ['name', 'description', 'funding']
    ordering = ['name']