from django.contrib import admin
from .models import TraitEntity, TraitAttribute, VarTrait, VarMethod, VarScale, Variable, SopDocument, AgroProcess

# Register your models here.
# Ontological Models
admin.site.register(TraitEntity)
admin.site.register(TraitAttribute)
admin.site.register(VarTrait)
admin.site.register(VarMethod)
admin.site.register(VarScale)
admin.site.register(Variable)
admin.site.register(SopDocument)
admin.site.register(AgroProcess)