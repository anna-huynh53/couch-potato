from django import forms
# Not 100% sure if we need this, it gives us the option of using form classes to represent the data submitted through a
# form, but at the moment the view is just directly accessing the data with the request.POST.get("Whatever") method
# If we ever use this file it'd probably be for the user sign up or something


class SearchForm(forms.Form):
    movie_search = forms.CharField(label='movie-search', max_length=200)