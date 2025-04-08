from django.urls import include, path
from django.contrib import admin

# In order to have seperate url files, django requires this file and to import the urls here:
from newgameplus.urls import demo_urls
from newgameplus.urls import game_urls
from newgameplus.urls import steam_urls

# All URL routes are defined here
urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include(demo_urls)),
    path('games/', include(game_urls)),
    path('steam/', include(steam_urls)),
]