from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


# Create your views here.
def home(request):
    content = 'Some text'
    return render(request, '../templates/home.html', {"bodyContent" : content})


def lists(request):
    content = 'Some text'
    return render(request, '../templates/lists.html', {"bodyContent" : "List stuff"})
