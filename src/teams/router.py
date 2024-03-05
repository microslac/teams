from django.conf import settings
from django.urls import include
from django.urls import re_path as url
from rest_framework import routers

from teams.views import InternalViewSet, TeamViewSet

app_name = settings.APP_TEAMS
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"teams", TeamViewSet, basename="Team")
router.register(r"internal", InternalViewSet, basename="Internal")

urlpatterns = [
    url(r"^", include(router.urls)),
]
