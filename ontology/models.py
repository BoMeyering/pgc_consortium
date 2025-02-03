"""
Data Ontology Models
"""

from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError

# App imports
from config.enumerations import VariableType, ScaleType
from config.custom_fields import KsuidField

""" Ontological Terms """
class TraitEntity(models.Model):
    """
    Entity model holds the label information about a specific trait entity object
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='traitEntity_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    abbreviation = models.CharField(max_length=30, unique=True, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Trait entities"

    def __str__(self):
        return self.label

class TraitAttribute(models.Model):
    """
    Attribute model holds the label information about a specific trait attribute object
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='traitAttr_')
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    abbreviation = models.CharField(max_length=30, unique=True, blank=False, null=False)
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
    abbreviation = models.CharField(max_length=50, unique=True, blank=False, null=False)
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
    abbreviation = models.CharField(max_length=50, unique=True, blank=False, null=False)
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
    abbreviation = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500)
    is_ordered = models.BooleanField(blank=False, null=False)
    type = models.CharField(max_length=50, choices=ScaleType, blank=False, null=False)
    external_ontology_reference = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.label
    
class ScaleValue(models.Model):
    """
    
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='scaleValue_')
    label = models.CharField(max_length=255, unique=False, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    var_scale = models.ForeignKey(
        VarScale, 
        on_delete=models.CASCADE, 
        blank=False, 
        null=False,
        limit_choices_to={'type__in': ['nominal', 'ordinal']}
    )

    class Meta:
        ordering = ['var_scale', 'order']
        constraints = [
            models.UniqueConstraint(fields=['var_scale', 'label', 'order'], name='scale_value_unique_constraint'),
            models.UniqueConstraint(fields=['var_scale', 'order'], name='scale_value_scale_order_unique_constraint'),
            models.UniqueConstraint(fields=['var_scale', 'label'], name='scale_value_scale_label_unique_constraint')
        ]
    
    def clean(self, *args, **kwargs):
        """
        
        """
        print("cleaning")
        super().clean(*args, **kwargs)

        # Check if VarScale is set
        if not self.var_scale:
            print("NO SCALE SET")
            raise ValidationError(f"var_scale cannot be empty")
        
        # Check that VarScale is nominal or ordinal
        if self.var_scale.type not in ['nominal', 'ordinal']:
            raise ValidationError(f"Cannot add a scale value to a non-ordinal/nominal scale")
        
        # Check if the VarScale is an ordered scale
        if self.var_scale.is_ordered:
            print("Working with an ordinal scale")
            # Query to get the maximum order or set to zero
            max_order = ScaleValue.objects.filter(var_scale=self.var_scale).aggregate(models.Max('order'))['order__max'] or 0
            if self.order is None:
                self.order = max_order + 1
            elif self.order <= 0:
                raise ValidationError(f"The order integer must be positive")
            elif (self.order < max_order) or (self.order - max_order > 1):
                raise ValidationError(f"The current highest order in this scale is {max_order}. The next scale value in the sequence must be {max_order + 1}")
            
        # Check if VarScale is unordered but an ordered scale value was passed
        elif (not self.var_scale.is_ordered) and (self.order):
            print("Cannot add an ordered scale value to an unordered scale")
            raise ValidationError(f"Cannot add an ordered scale value to an unordered scale")
        
        self.is_cleaned = True


    def save(self, *args, **kwargs):
        print("hello")
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['label', 'type'], name='variable_label_type_composite_key')
        ]
    
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
    version = models.CharField(max_length=8, blank=False, null=False)
    doi = models.URLField(blank=False, null=False)
    doc_url = models.URLField(blank=False, null=False)
    description = models.TextField(max_length=500, blank=False)
    variable_id = models.ForeignKey(Variable, on_delete=models.CASCADE, blank=True, null=True, related_name='sop_documents')

    class Meta:
        ordering = ['label']

    def truncate_description(self):
        """Return a truncated description for displaying in the tables"""
        if len(self.description) > 100:
            return format_html('{}...', self.description[:100])
        return self.description

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

    class Meta:
        verbose_name_plural = "Agro processes"

    def __str__(self):
        return self.label
    