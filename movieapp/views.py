from django.shortcuts import render
from .forms import SearchForm
from django.http import HttpResponseRedirect, HttpResponseNotFound


# Create your views here.
def home(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/results')

    else:
        form = SearchForm

    content = 'Some text'
    return render(request, '../templates/home.html', {"bodyContent" : content})


def lists(request):
    content = 'Some text 2'
    return render(request, '../templates/lists.html', {"bodyContent" : "List stuff"})


def results(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

    return render(request, '../templates/results.html', {"query": request.POST.get('movie-search') })


