from django.shortcuts import render

# Create your views here.
def list_variables(request):

    return render(
        request, 
        'ontology/variables.html',
        {}
    )

def manage_ontology(request):

    return render(
        request, 
        'ontology/manage.html',
        {}
    )

def import_ontology(request):

    return render(
        request, 
        'ontology/import.html',
        {}
    )


def list_sop(request):

    return render(
        request, 
        'ontology/sop.html',
        {}
    )

