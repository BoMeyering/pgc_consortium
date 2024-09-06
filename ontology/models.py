"""
Data Ontology Models
"""

from django.db import models

# App imports
from config.enumerations import VariableType
from config.custom_fields import KsuidField


# Create your models here.

""" Ontological Terms """
class TraitEntity(models.Model):
    """
    Entity model holds the label information about a specific trait entity object
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='traitEntity_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class TraitAttribute(models.Model):
    """
    Attribute model holds the label information about a specific trait attribute object
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='traitAttr_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class VarTrait(models.Model):
    """
    Trait model holds the specific trait identity for a given variable.
    FK on TraitEntity
    FK on TraitAttrribute
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='varTrait_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    entity_id = models.ForeignKey(TraitEntity, on_delete=models.CASCADE, blank=False, null=False)
    attribute_id = models.ForeignKey(TraitAttribute, on_delete=models.CASCADE, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class VarMethod(models.Model):
    """
    Method model holds variable method label and descriptions
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='varMethod_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class VarScale(models.Model):
    """
    Scale model holds variable scale label and descriptions
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='varScale_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label

class Variable(models.Model):
    """
    Variable model for the ontology
    FK1 on VarTrait
    Fk2 on VarMethod
    FK3 on VarScale
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='variable_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    abbreviation = models.CharField(max_length=255, unique=True, blank=False, null=False)
    trait_id = models.ForeignKey(VarTrait, on_delete=models.CASCADE, blank=False, null=False)
    method_id = models.ForeignKey(VarMethod, on_delete=models.CASCADE, blank=False, null=False)
    scale_id = models.ForeignKey(VarScale, on_delete=models.CASCADE, blank=False, null=False)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=VariableType, blank=False, null=False)
    
    def __str__(self):
        return f"{self.label} - ({self.abbreviation})"
    
class SopDocument(models.Model):
    """
    SOP Document model
    FK on Variable
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='sop_')
    document_name = models.CharField(max_length=255, blank=False, null=False)
    label = models.CharField(max_length=255, blank=False, null=True)
    doi = models.CharField(max_length=255, blank=False)
    url = models.URLField(blank=False, null=True)
    variable_id = models.ForeignKey(Variable, on_delete=models.CASCADE, blank=True, null=True, related_name='sop_documents')

    def __str__(self):
        return self.label
   
class AgroProcess(models.Model):
    """
    Agronomic process model
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='agroProcess_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    external_id = models.CharField(max_length=255, null=False, blank=False)
    external_reference = models.URLField()

    def __str__(self):
        return self.label
    