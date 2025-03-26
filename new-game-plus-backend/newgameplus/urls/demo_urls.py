from django.urls import path
from newgameplus.views import demo_views

# URL routes for the demo views
urlpatterns = [
    path('demo_get_request/', demo_views.demo_get_request, name='demo_get_request'),
]