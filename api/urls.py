"""
API Router URLs
"""

from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    # path('', views.ApiRoot.as_view(), name='api_root'),
    path('people', views.PersonList.as_view(), name='list_people'),
    path('people/<str:db_id>', views.PersonDetail.as_view(), name='list_person'),
    path('plots', views.PlotList.as_view(), name='list_plots')
]

# Formatting api url suffixes
urlpatterns = format_suffix_patterns(urlpatterns)