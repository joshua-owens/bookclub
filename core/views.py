from django.shortcuts import render

# Create your views here.
from django.views import View
from inertia import render

def index(request):
    return render(request, 'Home', props={
        'data': 'test'
    })

