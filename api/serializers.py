"""
API Serializers
"""

from rest_framework import serializers
from resources.models import Location, Person, Organization, Project
from data_storage.models import Plot, Trial, Treatment
from ontology.models import TraitEntity, TraitAttribute, VarTrait, VarMethod, VarScale, Variable, SopDocument, AgroProcess
from imaging.models import AwsModel, Image, ImageOperation

###### Name Serializers ######
class LocationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'db_id',
            'name'
        ]

class PersonNameSerializer(serializers.ModelSerializer):
    """
    API serializer for Manager name
    """
    class Meta:
        model = Person
        fields = [
            'db_id',
            'first_name',
            'middle_initial',
            'last_name'
        ]

class OrganizationNameSerializer(serializers.ModelSerializer):
    """
    API serializer for Organization name
    """
    class Meta:
        model = Organization
        fields = [
            'db_id',
            'name'
            ]

class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'db_id',
            'name'
        ]

class TrialNameSerializer(serializers.ModelSerializer):
    """
    API serializer for Trial name
    """
    class Meta:
        model = Trial
        fields = [
            'db_id',
            'name'
        ]

class TreatementNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = [
            'db_id',
            'name'
        ]

###### Resources Model Serializers ######
class LocationSerializer(serializers.ModelSerializer):
    """
    API serializer for Location
    """
    class Meta:
        model = Location
        fields = '__all__'
        
class PersonSerializer(serializers.ModelSerializer):
    """
    API serializer for Person
    """
    class Meta:
        model = Person
        fields = '__all__'

class OrganiztionSerializer(serializers.ModelSerializer):
    """
    API serializer for Organization
    """
    class Meta:
        model = Organization
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    """
    API serializer for Project
    """
    # Grab the related trials
    # project_trials = TrialNameSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

######### Data Storge Model Serializers #########
class PlotSerializer(serializers.ModelSerializer):
    """
    API serializer for Plot
    """
    # Instantiate the children Plot objects
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Plot.objects.all())

    class Meta:
        model = Plot
        fields = '__all__'

class TrialSerializer(serializers.ModelSerializer):
    """
    API serializer for Trial
    """

    # Related
    affiliation_id = OrganizationNameSerializer()
    manager_id = PersonNameSerializer()
    project_id = ProjectNameSerializer()

    class Meta:
        model = Trial
        # fields = '__all__'
        fields = [
            'db_id',
            'name',
            'project_id',
            'affiliation_id',
            'manager_id',
        ]

class TreatmentSerializer(serializers.ModelSerializer):
    """
    API serializer for Treatment
    """
    class Meta:
        model = Treatment
        fields = '__all__'

######### Ontology Model Serializers #########
class TraitEntitySerializer(serializers.ModelSerializer):
    """
    API serializer for TraitEntity
    """
    class Meta:
        model = TraitEntity
        fields = '__all__'

class TraitAttributeSerializer(serializers.ModelSerializer):
    """
    API serializer for TraitAttribute
    """
    class Meta:
        model = TraitAttribute
        fields = '__all__'

class VarTraitSerializer(serializers.ModelSerializer):
    """
    API serializer for VarTrait
    """
    class Meta:
        model = VarTrait
        fields = '__all__'

class VarMethodSerializer(serializers.ModelSerializer):
    """
    API serializer for VarMethod
    """
    class Meta:
        model = VarMethod
        fields = '__all__'

class VarScaleSerializer(serializers.ModelSerializer):
    """
    API serializer for VarScale
    """
    class Meta:
        model = VarScale
        fields = '__all__'

class VariableSerializer(serializers.ModelSerializer):
    """
    API serializer for Variable
    """
    class Meta:
        model = Variable
        fields = '__all__'

class SopDocumentSerializer(serializers.ModelSerializer):
    """
    API serializer for SopDocument
    """
    class Meta:
        model = SopDocument
        fields = '__all__'

class AgroProcessSerializer(serializers.ModelSerializer):
    """
    API serializer for AgroProcess
    """
    class Meta:
        model = AgroProcess
        fields = '__all__'

###### Imaging Model Serializers ######
class AwsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwsModel
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ImageOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageOperation
        fields = '__all__'

