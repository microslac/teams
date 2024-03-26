from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response
from teams.serializers import TeamSerializer, JoinTeamSerializer
from teams.services import TeamService


class TeamViewSet(BaseViewSet):
    @post(url_path="join")
    def join(self, request):
        data = request.data.copy()
        data.update(auth=request.token.auth)
        serializer = JoinTeamSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, auth_id = serializer.extract("team", "auth")
            team = TeamService.join_team(team_id, auth_id)
            resp = dict(team=TeamSerializer(team).data)
            return Response(resp, status=status.HTTP_200_OK)
