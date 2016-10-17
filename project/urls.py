"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from movieapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls), # ignore this
    url(r'^$', views.home, name='home'),
    url(r'randomMovies$', views.randomMovies, name='randomMovies'),
    url(r'randomTVShows$', views.randomTVShows, name='randomTVShows'),
    url(r'^results$', views.results, name='results'),
    url(r'^movie$', views.movie, name='movie'),
    url(r'myProfile$', views.myProfile, name='myProfile'),
    url(r'myProfile.html$', views.myProfile, name='myProfile'),
    url(r'editProfile$', views.editProfile, name='editProfile'),
    url(r'editProfile.html$', views.editProfile, name='editProfile'),
    url(r'^lists$', views.lists, name='lists'),
    url(r'^friends$', views.friends, name='friends'),
    url(r'^recommendations$', views.recommendations, name='recommendations'),
    url(r'^chicken_nugget$', views.chicken_nugget, name='chicken_nugget'),
]
