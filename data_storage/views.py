from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView

from .models import Location, State, Organization, Person, Address
from .models import Project, Trial, TrialYear, TrialAttribute
from .models import Treatment, TreatmentLevel, TrialTreatment
from .models import CommonName, Germplasm, GermplasmAlias
from .models import Plot, PlotCrop, PlotTreatment
from .models import TraitEntity, TraitAttribute, VarTrait, VarMethod, VarScale, Variable
from .models import Observation
from .models import AwsModel, Image, ImageOperation

from .forms import EmailContactForm


# Create your views here.
def index_view(request):

    return render(
        request, 
        'index.html'
    )


def list_states_locations(request):
    locations = Location.objects.all()
    states = State.objects.all()

    return render(
        request, 
        'data_storage/locations/states-and-locations.html',
        {'locations': locations, 
         'states': states}
    )

def show_state(request, abbreviation):
    try:
        state = State.objects.get(abbreviation=abbreviation)
    except State.DoesNotExist:
        raise Http404("Oops we couldn't find that state, this is embarassing")
    
    return render(
        request, 
        'data_storage/locations/show-state.html',
        {'state': state}
    )

def show_location(request, id):
    try:
        location = Location.objects.get(db_id=id)
    except Location.DoesNotExist:
        raise Http404("Oops we couldn't find that location, this is embarassing")
    
    return render(
        request, 
        'data_storage/locations/show-location.html', 
        {'location': location}
    )

def paginate_locations(request):
    location_list = Location.objects.all()
    paginator = Paginator(location_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        locations = paginator.page(page_number)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)

    return render(
        request, 
        'data_storage/locations/list.html', 
        {'locations': locations}
    )

class PaginateLocations(ListView):
    """
    Paginate Locations Class
    """

    queryset = Location.objects.all()
    context_object_name = 'locations'
    paginate_by = 4
    template_name = 'data_storage/locations/list.html'

def email_location(request, db_id):
    location = get_object_or_404(
        Location, 
        db_id=db_id
    )

    sent = False

    if request.method == 'POST':
        form = EmailLocationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            location_url = request.build_absolute_uri(
                location.get_absolute_url()
            )
            subject = (cd['subject'])
            message = (cd['message'])
            
            send_mail(
                subject=subject,
                message=message,
                from_email=None, 
                recipient_list=[cd['to']]
            )
            sent = True
        else:
            print("Form data is invalid")

        print(sent)

    else:
        form = EmailLocationForm()
    
    return render(
        request, 
        'data_storage/locations/show-location.html',
        {
            'location': location,
            'form': form,
            'sent': sent
        }
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
