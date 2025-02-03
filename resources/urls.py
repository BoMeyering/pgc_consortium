"""
resource app urls
"""

from django.urls import path, reverse
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_index, name='resource_index'),
    path('organizations', views.list_organizations, name='list_organizations'),
    path('organizations/<slug:slug>', views.organization_detail, name='organization_detail'),
    path('projects', views.manage_projects, name='manage_projects'),
    path('projects/create', views.create_project, name='create_project'),
    path('projects/<slug:slug>', views.project_detail, name='project_detail'),
    path('address-book', views.list_addresses, name='list_addresses'),
    path('people', views.list_people, name='list_people'),
    path('people/<slug:slug>', views.person_detail, name='person_detail'),
    path('contact-us', views.contact_us, name='contact_us')
]