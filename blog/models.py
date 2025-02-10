"""
Blog Models to handle social engagement on the website
"""

from django.db import models
from config.custom_fields import KsuidField
from resources.models import Project
from django.utils.text import slugify

class Publication(models.Model):
    """
    Publication model
    """

    db_id = KsuidField(primary_key=True, editable='False', prefix='publication_')
    title = models.CharField()
    doi = models.URLField()
    date = models.DateField()
    authors = models.CharField()
    journal = models.CharField()
    volume = models.CharField()
    issue = models.CharField()
    pages = models.CharField()

    def __str__(self):
        return self.title

class Post(models.Model):
    """
    Post model to handle blog posts
    """

    db_id = KsuidField(primary_key=True, editable=False, prefix='post_')
    title = models.CharField()
    subtitle = models.CharField()
    text = models.TextField()
    project_id = models.ForeignKey('resources.Project', on_delete=models.CASCADE, null=False, blank=False)
    publication_id = models.ForeignKey(Publication, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify([self.title])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    """
    Tag model to handle tags
    """

    db_id = KsuidField(primary_key=True, editable=False, prefix='posttag_')
    tag = models.CharField(null=False, blank=False)

    def __str__(self):
        return self.tag
    
class PostTag(models.Model):
    """
    Post Tag join table to handle post and tag relations
    """

    db_id = KsuidField(primary_key=True, editable=False, prefix='posttag_')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, null=False, blank=False)




