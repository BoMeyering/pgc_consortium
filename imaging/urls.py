"""
imaging app urls
"""

from django.urls import path, reverse
from . import views

app_name = 'imaging'

urlpatterns = [
    path('deployed-models', views.list_models, name='list_models'),
    path('manage', views.manage_images, name='manage_images'),
    path('model-output', views.view_output, name='view_output')
]