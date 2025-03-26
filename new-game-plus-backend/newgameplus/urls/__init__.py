from django.urls import include, path
from django.contrib import admin

# In order to have seperate url files, django requires this file and to import the urls here:
# EXAMPLE: from newgameplus.urls import auth_urls

# All URL routes are defined here
urlpatterns = [
    path('admin/', admin.site.urls),
    # EXAMPLE: path('auth/', include(auth_urls)),
]