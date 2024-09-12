from django.contrib import admin

# Register your models here.
from .models import Trial, TrialYear, TrialAttribute, TrialEvent
from .models import Treatment, TreatmentLevel, TrialTreatment
from .models import CommonName, Germplasm, GermplasmAlias
from .models import Plot, PlotCrop, PlotTreatment
from .models import Observation

from config.filters import ManagerFilter, TrialYearFilter, PlotCropFilter

""" Trial Models """
@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_id', 'affiliation_id', 'manager_id', 'establishment_year', 'multi_year']
    list_filter = ['establishment_year', 'multi_year', 'affiliation_id', 'project_id', ManagerFilter]

@admin.register(TrialYear)
class TrialYearAdmin(admin.ModelAdmin):
    list_display = ['trial_id', 'year']
    list_filter = ['trial_id', TrialYearFilter]
    ordering = ['trial_id', 'year']
    search_fields = ['trial_id', 'year']
    show_facets = admin.ShowFacets.ALWAYS

admin.site.register(TrialAttribute)
admin.site.register(TrialEvent)

""" Treatment Models """
@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'truncate_description']
    list_filter = ['type']
    ordering = ['name']

@admin.register(TreatmentLevel)
class TreatmentLevelAdmin(admin.ModelAdmin):
    list_display = ['treatment_id', 'level']
    list_filter = ['treatment_id']
    ordering = ['treatment_id', 'level']

@admin.register(TrialTreatment)
class TrialTreatment(admin.ModelAdmin):
    list_display = ['trial_id', 'treatment_id']
    list_filter = ['trial_id', 'treatment_id']
    search_fields = ['trial_id']
    ordering = ['trial_id', 'treatment_id']

""" Germplasm Models """
admin.site.register(CommonName)
admin.site.register(Germplasm)
admin.site.register(GermplasmAlias)

""" Plot Models """
@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ['label', 'trial_id', 'block', 'type', 'width_m', 'length_m', 'parent_plot_id', 'location_id']
    list_filter = ['trial_id', 'block', 'type', 'parent_plot_id']
    search_fields = ['trial_id', 'label', 'location_id']
    ordering = ['trial_id', 'label', 'type']

@admin.register(PlotCrop)
class PlotCropAdmin(admin.ModelAdmin):
    list_display = ['plot_id', 'plot_year', 'germplasm_id']
    list_filter = ['germplasm_id', PlotCropFilter]
    search_fields = ['plot_year', 'plot_id', 'germplasm_id']
    ordering = ['plot_year', 'plot_id']

admin.site.register(PlotTreatment)

""" Observation Models """
admin.site.register(Observation)
