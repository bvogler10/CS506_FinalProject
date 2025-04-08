from django.urls import path
from newgameplus.views import steam_views

# URL routes for the Steam API views
urlpatterns = [
    path('get_owned_games/', steam_views.get_owned_games, name='get_owned_games'),
]
