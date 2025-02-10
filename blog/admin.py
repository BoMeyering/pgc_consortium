from django.contrib import admin

# Register your models here.
from .models import Post, PostTag, Publication, Tag

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):

admin.site.register(Post)
admin.site.register(PostTag)
admin.site.register(Publication)
admin.site.register(Tag)
