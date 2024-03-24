from micro.jango.views import unauthorized
from django.urls import include
from django.urls import re_path as url

urlpatterns = [
    url(r"^$", unauthorized, name="403"),
    url(r"^", include("teams.router", namespace="teams")),
]
