"""
Data_Storage Views
"""

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView

from .models import Trial, TrialYear, TrialAttribute
from .models import Treatment, TreatmentLevel, TrialTreatment
from .models import CommonName, Germplasm, GermplasmAlias
from .models import Plot, PlotCrop, PlotTreatment
from .models import Observation

from .forms import EmailContactForm


# Create your views here.
def index_view(request):

    return render(
        request, 
        'index.html'
    )

def list_projects(request):

    return render(
        request, 
        'data_storage/management/list_projects.html',
        {}
    )

def list_trials(request):

    return render(
        request, 
        'data_storage/management/list_trials.html',
        {}
    )

def list_plots(request):

    return render(
        request, 
        'data_storage/management/list_plots.html',
        {}
    )

def view_data(request):

    return render(
        request, 
        'data_storage/observations/view_data.html',
        {}
    )

def analyze_data(request):

    return render(
        request, 
        'data_storage/observations/analyze_data.html',
        {}
    )

def graph_data(request):

    return render(
        request, 
        'data_storage/observations/graph_data.html',
        {}
    )

def list_locations(request):

    return render(
        request, 
        'data_storage/management/list_locations.html',
        {}
    )
