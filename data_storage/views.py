"""
Data_Storage Views
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView

from .models import Trial, TrialYear, TrialAttribute
from .models import Treatment, TreatmentLevel, TrialTreatment
from .models import CommonName, Germplasm, GermplasmAlias
from .models import Plot, PlotCrop, PlotTreatment
from .models import CropObservation
from .forms import NewTrialForm

from resources.models import Project

from data_storage.services import export_plots_to_csv

from .forms import EmailContactForm, TrialFilterForm


# Create your views here.
def index_view(request):

    return render(
        request, 
        'index.html'
    )

def list_projects(request):

    return render(
        request, 
        'data_storage/field_management/list_projects.html',
        {}
    )

def list_trials(request):

    trials = Trial.objects.all()

    return render(
        request, 
        'data_storage/field_management/list_trials.html',
        {'trials': trials}
    )

def create_trial(request):

    project_slug = request.GET.get('project', None)
    if project_slug:
        project = Project.objects.get(slug=project_slug)
    else:
        project = None

    if request.method == 'POST':
        form = NewTrialForm(request.POST)
        if form.is_valid():
            form.save()
            instance = form.instance
            
            return redirect('data_storage:list_trials')

    else:
        form = NewTrialForm()

    context = {
        'form': form,
        'project': project
    }

    return render(
        request,
        'data_storage/field_management/create_trial.html',
        context
    )

def list_plots(request):
    plots = Plot.objects.all()
    form = TrialFilterForm(request.POST or None)

    if form.is_valid():
        selected_trials = form.cleaned_data['trials']
        plots = Plot.objects.filter(trial_id__in=selected_trials)

        # paginator = Paginator(plots, 10)
        # page_number =request.GET.get('page', 1)
        # try:
        #     plots = paginator.page(page_number)
        # except EmptyPage:
        #     plots = paginator.page(paginator.num_pages)

        if 'export' in request.POST:
            print(True)
            return export_plots_to_csv(plots)
        
        return render(
            request, 
            'data_storage/field_management/list_plots.html',
            {
                "form": form,
                "trials": selected_trials, 
                "plots": plots
            }
        )
    
    
    
    return render(
        request, 
        'data_storage/field_management/list_plots.html',
        {
            "form": form,
            "plots": plots
        }
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
        'data_storage/field_management/list_locations.html',
        {}
    )

def logbook(request):

    return render(
        request, 
        'data_storage/field_management/logbook.html',
        {}
    )