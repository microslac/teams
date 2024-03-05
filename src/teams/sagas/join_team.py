from micro.events.publishers.registry import communication
from micro.patterns.saga import Saga, State, Step
from micro.services.registry import AuthService, ConversationsService, UsersService


class InfoAuth(Step):
    def action(self):
        data = dict(id=self.state.auth.id)
        auth = AuthService.post("/internal/info", data=data, key="auth", objectify=True)
        self.state.auth = auth


class CreateUser(Step):
    def action(self):
        email = self.state.auth.email
        name = email.split("@").pop(0)
        data = dict(team=self.state.team.id, auth=self.state.auth.id, email=email, name=name)
        user = UsersService.post("/internal/create", data=data, key="user", objectify=True)
        self.state.user = user

    def compensate(self):
        data = dict(user=self.state.user.id, team=self.state.team.id)
        UsersService.post("/internal/destroy", data=data)


class JoinBaseChannel(Step):
    def __init__(self, is_general: bool = False, is_random: bool = False):
        self.is_general = is_general
        self.is_random = is_random
        self.channel = State()

    def action(self):
        data = dict(
            team=self.state.team.id,
            user=self.state.user.id,
            is_general=self.is_general,
            is_random=self.is_random,
        )
        channel = ConversationsService.post("/internal/join", data=data, key="channel", objectify=True)
        self.channel = channel

    def compensate(self):
        data = dict(team=self.state.team.id, user=self.state.user.id, channel=self.channel.id)
        ConversationsService.post("/internal/kick", data=data)


class JoinTeamSaga(Saga):
    def __init__(self, team_id: str, auth_id: str, verbose: bool = False):
        self.state.team = State(id=team_id)
        self.state.auth = State(id=auth_id)
        self.verbose = verbose

        self.steps = [
            InfoAuth(),
            CreateUser(),
            JoinBaseChannel(is_general=True),
            JoinBaseChannel(is_random=True),
        ]

    def on_success(self):
        payload = dict(auth=self.state.auth.id, team=self.state.team.id, user=self.state.user.id)
        communication.publish(payload, routing_key="team.user.joined")
