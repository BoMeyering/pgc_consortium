"""
API Serializers
"""

from rest_framework import serializers
from resources.models import Person
from data_storage.models import Plot

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class PlotSerializer(serializers.ModelSerializer):

    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Plot.objects.all())

    class Meta:
        model = Plot
        fields = '__all__'
        # fields = [
        #     'db_id',
        #     'label', 
        #     'block', 
        #     'row',
        #     'column',
        #     'length_m',
        #     'width_m', 
        #     'parent_plot_id',
        #     'type',
        #     'trial_id',
        #     'children'
        # ]