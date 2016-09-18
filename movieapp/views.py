from django.shortcuts import render
from .forms import SearchForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
import json
import requests
from .models import User

# Home page
def home(request):

    if request.method == 'POST':
        # unreachable code??

        # testing if I can access the email
        if 'email' in request.POST:

            request.session['loggedIn'] = True  # specify that a user is logged in

            try:
                user = User.objects.get(email=request.POST['email'])
            except:
                print("OOK")
                newUser = User(firstName=request.POST['firstName'], familyName=request.POST['familyName'], email=request.POST['email'])
                newUser.save()
                request.session['email'] = request.POST['email']

            return render(request, '../templates/results.html', {"movie": request.POST['email']})
        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/results')

    else:
        form = SearchForm

        if request.session.get('loggedIn'):
            content = request.session['email']
        else:
            content = 'Search'
        return render(request, '../templates/home.html', {"bodyContent" : content})


# Personal lists (if this is still it's own page I'm not sure)
def lists(request):
    if request.session.get('loggedIn'):

        currentUser = User.objects.get(email=request.session.get('email'))
        return render(request, '../templates/lists.html', {"currentUserRecord": currentUser, "bodyContent": "List:"})

    return render(request, '../templates/lists.html', {"bodyContent": "Error: Not logged in"})


# Search results
def results(request):

    # If this is a search
    if request.method == 'POST':

        if 'movie' in request.POST:
            # if the user has clicked "add to my watched list"
            movie = request.POST.get("movie")


        else:
            movie_query = request.POST.get('movie-search')  # gets query from POST data

            url = 'http://www.omdbapi.com/?s=' + movie_query
            response = requests.get(url)
            content = json.loads(response.text)
            raw_items = content["Search"]

            class Movie:
                def __init__(self, title, year, ID):
                    self.title = title
                    self.year = year
                    self.imdbID = ID

            movies = []

            # TODO make item some kind of object which includes imdbID so when clicked, it can link to more detailed info
            for item in raw_items:
                movies.append(Movie(item["Title"], item["Year"], item["imdbID"]))

            # TODO rename query
            return render(request, '../templates/results.html', {"query": movies})

    # if this is a clicked movie link
    # TODO move this to a different view, a 'movie' view I would imagine
    elif request.method == 'GET':
        url = 'http://www.omdbapi.com/?i=' + request.GET["id"] + "&plot=full&r=json"
        response = requests.get(url)
        content = json.loads(response.text)

        class FullMovie:
            def __init__(self, content):
                # there is almost certainly a less retarded way of doing this
                self.title = content["Title"]
                self.year = content["Year"]
                self.rated = content["Rated"]
                self.released = content["Released"]
                self.runtime = content["Runtime"]
                self.genre = content["Genre"]
                self.director = content["Director"]
                self.writer = content["Writer"]
                self.actors = content["Actors"]
                self.plot = content["Plot"]
                self.language = content["Language"]
                self.country = content["Country"]
                self.poster = content["Poster"]
                self.metascore = content["Metascore"]
                self.imdbRating = content["imdbRating"]
                self.response = content["Response"]

        movie = FullMovie(content)

        return render(request, '../templates/movie.html', {"movie": movie})

