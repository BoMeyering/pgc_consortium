"""
data_storage app urls
"""

from django.urls import path, reverse
from . import views

app_name = 'data_storage'

urlpatterns = [
    path('field-management/projects', views.list_projects, name='list_projects'),
    path('field-management/trials', views.list_trials, name='list_trials'),
    path('field-management/plots', views.list_plots, name='list_plots'),
    path('field-management/locations', views.list_locations, name='list_locations'),
    # path('field-management/locations', views.list_states_locations, name='locations_list'),
    path('observations/data', views.view_data, name='view_data'),
    path('observations/analyze', views.analyze_data, name='analyze_data'),
    path('observations/graph', views.graph_data, name='graph_data'),
    # path('locations/states/<slug:abbreviation>', views.show_state, name='show_state'),
    # path('locations/<slug:id>', views.show_location, name='show_location'),
    # path('locations/<slug:db_id>', views.email_location, name='show_location'),
    # path('locations-list/', views.paginate_locations, name='paginate_locations')
    # path('locations-list/', views.PaginateLocations.as_view(), name='paginate_locations'),
]