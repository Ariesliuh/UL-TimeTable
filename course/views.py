from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    module_id = request.GET['Module']
    return HttpResponse('Module ID:'+str(module_id))
