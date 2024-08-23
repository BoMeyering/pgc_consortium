"""
admin page custom filters
"""

from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from .models import Trial, Person

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