"""
Imaging and DL Model Database Models
"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_image_file_extension

from config.custom_fields import KsuidField
from config.enumerations import StatusType


""" AWS Models """
class AwsModel(models.Model):
    """
    AWS Model structure to record all different AWS models in the system
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='awsModel_')
    name = models.CharField(max_length=255, null=False, blank=False)
    version = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    endpoint_url = models.URLField(null=False, blank=False)

    def __str__(self):
        return f"{self.name} - {self.version}"

""" Image and File Storage """
class Image(models.Model):
    """
    Image model for determining the structure of images connected to a specific observation
    FK on Observation
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='image_')
    filename = models.CharField(
        max_length=255, 
        blank=False, 
        null=False, 
        validators=[
            validate_image_file_extension
        ]
    )
    height = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99999)
        ]
    )
    width = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99999)
        ]
    )
    creation_date_time = models.DateTimeField(blank=False, null=False)
    storage_url = models.URLField(blank=False, null=False)
    observation_id = models.ForeignKey('data_storage.Observation', on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        if self.observation_id:
            observation = self.observation_id
            return f"{self.filename} - {self.creation_date_time} - {self.observation_id.variable_id.label}"
        else:
            return f"{self.filename} - {self.creation_date_time} - No observations linked"

class ImageOperation(models.Model):
    """
    Image Operation model outlines the structure of individual operations performed on an image by a model
    FK1 on Image
    FK2 on AwsModel
    """
    db_id = KsuidField(primary_key=True, editable=False, prefix='imageOperation_')
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False, null=False)
    model_id = models.ForeignKey(AwsModel, on_delete=models.CASCADE, blank=False, null=False)
    date_time = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    status = models.CharField(max_length=50, choices=StatusType)

    def __str__(self):
        return f"{self.image_id} - {self.model_id} - {self.date_time}: {self.status}"

    
