"""
blog app urls
"""

from django.urls import path, reverse
from . import views

app_name = 'blog'

urlpatterns = [
    # path('blog/<slug:slug>', views.post_detail, name='post_detail'),
]