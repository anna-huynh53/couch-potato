from django.shortcuts import render
from .forms import SearchForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
import json
import requests

# Home page
def home(request):

    if request.method == 'POST':
        # unreachable code??
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/results')

    else:
        form = SearchForm

    content = 'Some text'
    return render(request, '../templates/home.html', {"bodyContent" : content})


# Personal lists (if this is still it's own page I'm not sure)
def lists(request):
    content = 'Some text 2'
    return render(request, '../templates/lists.html', {"bodyContent" : "List stuff"})


# Search results
def results(request):
    if request.method == 'POST':
        # form = SearchForm(request.POST) -- not sure how to get this method working or if it's even necessary
        movie_query = request.POST.get('movie-search')  # gets query from POST data

        url = 'http://www.omdbapi.com/?s=' + movie_query
        response = requests.get(url)
        content = json.loads(response.text)
        raw_items = content["Search"]

        items = []
        # TODO make item some kind of object which includes imdbID so when clicked, it can link to more detailed info
        for item in raw_items:
            items.append(item["Title"] + ' ' + item["Year"])

        # title = content["Title"]
        # year = content["Year"]

    return render(request, '../templates/results.html', {"query": items})


