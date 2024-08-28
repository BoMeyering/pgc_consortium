from django.shortcuts import render
from django.core.mail import send_mail

from .forms import ContactForm


# Create your views here.

def resource_index(request):

    return render(
        request, 
        'resources/index.html',
        {}
    )

def list_organizations(request):

    return render(
        request, 
        'resources/organizations.html',
        {}
    )

def manage_projects(request):

    return render(
        request, 
        'resources/projects.html',
        {}
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

def contact_us(request):

    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            subject = cd['subject']
            name = cd['name']
            email = cd['your_email']

            prefix = f"Name: {name}\nContact: {email}\nSubject: {subject}\n\n"

            message = prefix + cd['message']
            
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