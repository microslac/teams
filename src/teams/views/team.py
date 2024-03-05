from core.auth.permissions import IsInternal
from core.serializers import IdSerializer
from core.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from teams.serializers import TeamSerializer
from teams.services import TeamService


class TeamViewSet(BaseViewSet):
    @post(url_path="create")
    def create_(self, request):
        data = request.data.copy()
        data.update(creator=request.token.auth)
        serializer = TeamSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            creator_id = serializer.pop("creator")
            team = TeamService.create_team(creator_id=creator_id, data=serializer.validated_data)
            resp = dict(team=TeamSerializer(team).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="lookup", permission_classes=(IsInternal,))
    def lookup(self, request):
        data = request.data.copy()
        serializer = IdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if team := TeamService.lookup_team(data.pop("id")):
                return Response(dict(team=team), status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @post(url_path="destroy", permission_classes=(IsInternal,))
    def destroy_(self, request):
        data = request.data.copy()
        serializer = IdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            TeamService.destroy_team(data.pop("id"))
            return Response(status=status.HTTP_200_OK)

    @post(url_path="list")
    def list_(self, request):
        resp = [
            dict(id="T1", name="team"),
            dict(id="T2", name="next"),
        ]
        return Response(data=resp, status=status.HTTP_200_OK)