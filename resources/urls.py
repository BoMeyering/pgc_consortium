"""
resource app urls
"""

from django.urls import path, reverse
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_index, name='resource_index'),
    path('organizations', views.list_organizations, name='list_organizations'),
    path('projects', views.manage_projects, name='manage_projects'),
    path('address-book', views.list_addresses, name='list_addresses'),
    path('people', views.list_people, name='list_people'),
    path('contact-us', views.contact_us, name='contact_us')
]