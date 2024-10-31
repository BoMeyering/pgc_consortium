from django.contrib import admin
from .models import AwsModel
from .models import Image, ImageOperation

# Register your models here.

# AWS Models
admin.site.register(AwsModel)

# Image Models
admin.site.register(Image)
admin.site.register(ImageOperation)