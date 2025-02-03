from django.shortcuts import render, redirect
from django.core.mail import send_mail

from resources.models import Organization, Person, Project
from resources.forms import NewProjectForm
from data_storage.models import Trial
from .forms import ContactForm
from django.shortcuts import get_object_or_404


# Create your views here.

def resource_index(request):

    return render(
        request, 
        'resources/index.html',
        {}
    )

def list_organizations(request):
    organizations = Organization.objects.all()

    return render(
        request, 
        'resources/organizations.html',
        {'orgs': organizations}
    )

def organization_detail(request, slug):
    org = get_object_or_404(
        Organization, 
        slug=slug
    )

    trials = Trial.objects.filter(affiliation_id=org)

    people = Person.objects.filter(affiliation_id=org)
    print(people)

    return render(
        request, 
        'resources/organization_detail.html', 
        {
            "org": org, 
            "trials": trials,
            "people": people
        }
    )

def manage_projects(request):
    active_projects = Project.objects.filter(is_active=True)
    inactive_projects = Project.objects.filter(is_active=False)

    context = {
        'active_projects': active_projects,
        'inactive_projects': inactive_projects
    }

    return render(
        request, 
        'resources/projects.html',
        context
    )

def create_project(request):

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            instance = form.instance

            return redirect('resources:project_detail',
                            slug=instance.slug)
    else:
        form = NewProjectForm()

    context = {
        'form': form
    }

    return render(
        request, 
        'resources/create_project.html',
        context
    )

def project_detail(request, slug):

    project = get_object_or_404(
        Project,
        slug=slug
    )

    project_trials = project.project_trials.all()
    print(project_trials)


    context = {
        'project': project,
        'project_trials': project_trials
    }

    return render(
        request,
        'resources/project_detail.html',
        context
    )

def list_addresses(request):

    return render(
        request, 
        'resources/addresses.html',
        {}
    )

def list_people(request):

    return render(
        request, 
        'resources/people.html',
        {}
    )

def person_detail(request, slug):
    person = get_object_or_404(
        Person,
        slug=slug
    )

    return render(
        request,
        'resources/person_detail.html',
        {'person': person}
    )

def contact_us(request):

    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            subject = cleaned_data['subject']
            name = cleaned_data['name']
            email = cleaned_data['your_email']

            prefix = f"Name: {name}\nContact: {email}\nSubject: {subject}\n\n"

            message = prefix + cleaned_data['message']
            
            send_mail(
                subject=subject,
                message=message,
                from_email=None, 
                recipient_list=['bomeyering25@gmail.com', email]
            )
            sent = True
        else:
            print("Form data is invalid")

        print(sent)

    else:
        form = ContactForm()
    
    return render(
        request, 
        'data_storage/contact.html',
        {
            'form': form,
            'sent': sent
        }

    )