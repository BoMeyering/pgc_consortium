"""
admin page custom filters
"""

from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from resources.models import Person
from data_storage.models import Trial, TrialYear
from data_storage.models import PlotCrop

class ManagerFilter(admin.SimpleListFilter):
    title = _('Manager')
    parameter_name = 'manager_id'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        managers = Person.objects.filter(db_id__in=Trial.objects.values_list('manager_id', flat=True))
        
        return [(manager.db_id, f"{manager.first_name} {manager.last_name}") for manager in managers]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value():
            return queryset.filter(manager_id=self.value())
        return queryset
    

class TrialYearFilter(admin.SimpleListFilter):
    title = _('TrialYear')
    parameter_name = 'year'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        trial_years = TrialYear.objects.values_list('year', flat=True).distinct()

        return [(trial_year, trial_year) for trial_year in trial_years]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value():
            return queryset.filter(year=self.value())
        return queryset

class PlotCropFilter(admin.SimpleListFilter):
    title = _('PlotCropYear')
    parameter_name = 'plot_year'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        plot_years = PlotCrop.objects.values_list('plot_year', flat=True).distinct()

        return [(plot_year, plot_year) for plot_year in plot_years]
        
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value():
            return queryset.filter(plot_year=self.value())
        return queryset