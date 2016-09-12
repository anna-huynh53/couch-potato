from django import forms


class SearchForm(forms.Form):
    movie_search = forms.CharField(label='movie-search', max_length=200)