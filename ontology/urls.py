"""
ontology app urls
"""

from django.urls import path, reverse
from . import views

app_name = 'ontology'

urlpatterns = [
    path('variables', views.list_variables, name='list_variables'),
    path('manage', views.manage_ontology, name='manage_ontology'),
    path('import', views.import_ontology, name='import_ontology'),
    path('sop', views.list_sop, name='list_sop')
]