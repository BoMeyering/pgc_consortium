from django.shortcuts import render

# Create your views here.
def list_models(request):

    return render(
        request, 
        'imaging/list_models.html',
        {}
    )
def manage_images(request):

    return render(
        request, 
        'imaging/images.html',
        {}
    )

def view_output(request):

    return render(
        request, 
        'imaging/output.html',
        {}
    )