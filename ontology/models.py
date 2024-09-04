from ksuid import Ksuid
from django.db import models
from data_storage.models import Trial, VariableType

# Create your models here.

# """ ID Functions """
# def generate_ksuid():
#     """
#     Generate a K-Sorted Universal ID
#     """
#     return str(Ksuid())


# """ Enumerations """    
# class VariableType(models.TextChoices):
#     """
#     Enumerate the different variable types
#     """
#     CORN = 'corn', 'Corn'
#     SOYBEAN = 'soybean', 'Soybean'
#     PGC_GRASS = 'pgc grass', 'PGC Grass'
#     PGC_CLOVER = 'pgc clover', 'PGC Clover'
#     WEED = 'weed', 'Weed'
#     SOIL = 'soil', 'Soil'

# """ Ontological Terms """
# class TraitEntity(models.Model):
#     """
#     Entity model holds the label information about a specific trait entity object
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     external_ontology_reference = models.URLField(null=True, blank=True)
    
#     def __str__(self):
#         return self.label

# class TraitAttribute(models.Model):
#     """
#     Attribute model holds the label information about a specific trait attribute object
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     external_ontology_reference = models.URLField(null=True, blank=True)
    
#     def __str__(self):
#         return self.label

# class VarTrait(models.Model):
#     """
#     Trait model holds the specific trait identity for a given variable.
#     FK on TraitEntity
#     FK on TraitAttrribute
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     entity_id = models.ForeignKey(TraitEntity, on_delete=models.CASCADE, blank=False, null=False)
#     attribute_id = models.ForeignKey(TraitAttribute, on_delete=models.CASCADE, blank=False, null=False)
#     external_ontology_reference = models.URLField(null=True, blank=True)
    
#     def __str__(self):
#         return self.label

# class VarMethod(models.Model):
#     """
#     Method model holds variable method label and descriptions
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     description = models.TextField(max_length=500)
#     external_ontology_reference = models.URLField(null=True, blank=True)
    
#     def __str__(self):
#         return self.label

# class VarScale(models.Model):
#     """
#     Scale model holds variable scale label and descriptions
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     description = models.TextField(max_length=500)
#     external_ontology_reference = models.URLField(null=True, blank=True)
    
#     def __str__(self):
#         return self.label

# class Variable(models.Model):
#     """
#     Variable model for the ontology
#     FK1 on VarTrait
#     Fk2 on VarMethod
#     FK3 on VarScale
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     abbreviation = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     trait_id = models.ForeignKey(VarTrait, on_delete=models.CASCADE, blank=False, null=False)
#     method_id = models.ForeignKey(VarMethod, on_delete=models.CASCADE, blank=False, null=False)
#     scale_id = models.ForeignKey(VarScale, on_delete=models.CASCADE, blank=False, null=False)
#     sop_url = models.URLField(blank=True, null=True)
#     min_value = models.FloatField(blank=True, null=True)
#     max_value = models.FloatField(blank=True, null=True)
#     type = models.CharField(max_length=50, choices=VariableType, blank=False, null=False)
    
#     def __str__(self):
#         return f"{self.label} - ({self.abbreviation})"

# class AgroProcess(models.Model):
#     """
#     Agronomic process model
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     label = models.CharField(max_length=255, unique=True, blank=False, null=False)
#     description = models.TextField(max_length=500, null=False, blank=False)
#     external_id = models.CharField(max_length=255, null=False, blank=False)
#     external_reference = models.URLField()

#     def __str__(self):
#         return self.label
    
# class TrialEvent(models.Model):
#     """
#     Trial Event model, tracks trial level agronomic processes and dates
#     FK1 on Trial
#     FK2 on AgroProcess
#     """
#     db_id = models.CharField(default=Ksuid, primary_key=True, editable=False, unique=True)
#     trial_id = models.ForeignKey(Trial, on_delete=models.CASCADE, blank=False, null=False)
#     process_id = models.ForeignKey(AgroProcess, on_delete=models.CASCADE, blank=False, null=False)
#     date = models.DateField(default = date.today(), blank=False, null=False)
#     comment = models.TextField(max_length=500, blank=False, null=False)

#     def __str__(self):
#         return f"{self.trial_id.name} - {self.process_id.label}"