from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    course_id = request.GET['id']
    return HttpResponse('Module ID:'+str(course_id))
