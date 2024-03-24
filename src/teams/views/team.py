from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response


class TeamViewSet(BaseViewSet):
    @post(url_path="list")
    def list_(self, request):
        resp = dict(
            ok=True,
            teams=[
                dict(id="T1", name="team"),
                dict(id="T2", name="next"),
            ]
        )
        return Response(data=resp, status=status.HTTP_200_OK)
