"""
API Router URLs
"""

from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    # path('', views.ApiRoot.as_view(), name='api_root'),
    path('locations', views.LocationList.as_view(), name='list_locations'),
    path('people', views.PersonList.as_view(), name='list_people'),
    path('people/<str:db_id>', views.PersonDetail.as_view(), name='list_person'),
    path('plots', views.PlotList.as_view(), name='list_plots'),
    path('trials', views.TrialList.as_view(), name='list_trials'),
    path('treatments', views.TreatmentList.as_view(), name='list_treatments'),
    path('projects', views.ProjectList.as_view(), name='list_projects'),
    path('aws_models', views.AwsModelList.as_view(), name='list_aws_models'),
    path('image_operations/<str:db_id>', views.ImageOperationDetail.as_view(), name='list_image_operation')
]

# Formatting api url suffixes
urlpatterns = format_suffix_patterns(urlpatterns)