from django.shortcuts import render
from .forms import SearchForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
import json
import requests
from .models import User
from .models import Movie

# Home page
def home(request):

    if request.method == 'POST':
        # unreachable code??

        # testing if I can access the email
        if 'email' in request.POST:

            if 'password' in request.POST:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    if request.POST['password'] != user.password:
                        return render(request, '../templates/home.html', {"loggedIn": False})
                    else:
                        request.session['email'] = request.POST['email']
                        request.session['loggedIn'] = True
                        return render(request, '../templates/home.html', {"loggedIn": True})
                except:
                    return render(request, '../templates/home.html', {"loggedIn": False})

            else:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    request.session['email'] = request.POST['email']
                    print("user exists")
                except:
                    print("creating new user")
                    newUser = User(firstName=request.POST['firstName'], familyName=request.POST['familyName'], email=request.POST['email'])
                    newUser.save()
                    request.session['email'] = request.POST['email']

                request.session['loggedIn'] = True  # specify that a user is logged in

                return render(request, '../templates/home.html', {"loggedIn": True})

        elif 'user' in request.POST:

            try:
                userAdded = User.objects.get(email=request.POST['user'])
                userAdded.save()

                try:
                    user = User.objects.get(email=request.session['email'])
                    user.friends.add(userAdded)
                    user.save()
                    return render(request, '../templates/home.html', {"addStatus": "User Added!", "loggedIn": request.session['loggedIn']})
                except:
                    print("Some other error")
                    return render(request, '../templates/home.html', {"addStatus": "Error", "loggedIn": request.session['loggedIn']})
            except:
                print("actual user does not exist")
                return render(request, '../templates/home.html', {"addStatus": 'User Doesnt Exist!', "loggedIn": request.session['loggedIn']})


        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/results')

    else:

        if request.session.get('loggedIn'):
            content = request.session['email']
            user = User.objects.get(email=request.session.get('email'))
            watched = user.watchedList.all()
            toWatch = user.toWatchList.all()

            return render(request, '../templates/home.html', {"addStatus": "Email", "watched": watched, "toWatch": toWatch, "loggedIn": request.session['loggedIn']})
        else:
            content = 'Search'

            return render(request, '../templates/home.html', {"addStatus" : "Email", "loggedIn": False})


# Personal lists (if this is still it's own page I'm not sure)
def lists(request):
    if request.session.get('loggedIn'):

        currentUser = User.objects.get(email=request.session.get('email'))
        return render(request, '../templates/lists.html', {"currentUserRecord": currentUser, "bodyContent": "My List"})

    return render(request, '../templates/lists.html', {"bodyContent": "Error: Not logged in"})


# Search results
def results(request):

    # If this is a search
    if request.method == 'POST':

        if 'movie' in request.POST:
            # if the user has clicked "add to my watched list"
             movie = request.POST.get("movie")
            # newMovie = Movie(title=movie.title, year=movie.year, imdbID=movie.imdbID)
            # newMovie.save()
            #
            # user = User.objects.get(email=request.session.get('email'))
            # user.watchedList.add(movie)
            # user.save()
        else:
            movie_query = request.POST.get('search')  # gets query from POST data

        url = 'http://www.omdbapi.com/?s=' + movie_query
        response = requests.get(url)
        content = json.loads(response.text)
        raw_items = content["Search"]

        class Movie:
            def __init__(self, title, year, ID, poster):
                self.title = title
                self.year = year
                self.imdbID = ID
                self.poster = poster

        movies = []

        # TODO make item some kind of object which includes imdbID so when clicked, it can link to more detailed info
        for item in raw_items:
            movies.append(Movie(item["Title"], item["Year"], item["imdbID"], item["Poster"]))

        # TODO rename query
        return render(request, '../templates/movieResults.html', {"query": movies})


def movie(request):

    if request.method == 'GET':
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

        movieDict = FullMovie(content)

        return render(request, '../templates/movie.html', {"movie": movieDict})

    elif request.method == 'POST':

        movie = request.POST['movie']

        newMovieRecord = Movie(
            imdbID  = movie['imdbID'],
            title = movie['title'],
            year = movie['year'],
            rated = movie['rated'],
            released = movie['released'],
            runtime = movie['runtime'],
            genre =movie['genre'],
            director = movie['director'],
            writer = movie['writer'],
            actors = movie['actors'],
            plot = movie['plot'],
            language = movie['language'],
            country = movie['country'],
            poster = movie['poster'],
            metascore = movie['metascore'],
            imdbRating = movie['imdbRating'],
        )

        newMovieRecord.save()

        return render(request, '../templates/movie.html', {"movie": movie})


def friends(request):
    error = False
    if request.session.get('loggedIn'):
        currentUser = User.objects.get(email=request.session.get('email'))
        if request.method == 'POST':
            if request.POST.get("Unfollow"):
                try:
                    to_delete = User.objects.get(email=request.POST.get('Unfollow'))
                    currentUser.friends.remove(to_delete)
                    currentUser.save()
                except (KeyError, User.DoesNotExist):
                    print("")
            else:
                try:
                    to_add = User.objects.get(email=request.POST['add_friend'])
                    currentUser.friends.add(to_add)
                    currentUser.save()
                except (KeyError, User.DoesNotExist):
                    error = True

        userFriends = currentUser.friends.all()
        return render(request, '../templates/friends.html', {"friends": userFriends, 'error':error})

def editProfile(request):

    return render(request, '../templates/editProfile.html')
