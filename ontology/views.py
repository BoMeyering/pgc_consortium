from django.shortcuts import render
from data_storage.models import CommonName, Variable

# Create your views here.
def list_variables(request):

    return render(
        request, 
        'ontology/variables.html',
        {}
    )

def manage_ontology(request):

    common_names = CommonName.objects.all()

    try:
        corn_variables = Variable.objects.get(type='corn')
    except Variable.DoesNotExist:
        corn_variables = None

    try:
        soybean_variables = Variable.objects.get(type='soybean')
    except Variable.DoesNotExist:
        soybean_variables = None
    
    try:
        pgc_variables = Variable.objects.get(type='pgc')
    except Variable.DoesNotExist:
        pgc_variables = None

    try:
        soil_variables = Variable.objects.get(type='soil')
    except Variable.DoesNotExist:
        soil_variables = None

    add_vars = all(v is None for v in [corn_variables, soybean_variables, pgc_variables, soil_variables])
    print(add_vars)

    return render(
        request, 
        'ontology/manage.html',
        {'common_names': common_names,
         'corn_variables': corn_variables,
         'soybean_variables': soybean_variables,
         'pgc_variables': pgc_variables,
         'soil_variables': soil_variables,
         'add_vars': add_vars
         }
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

