from micro.patterns.saga import Saga, State, Step
from micro.services.registry import AuthService, ConversationsService, UsersService

from teams.services import TeamService


class CreateAuth(Step):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def action(self):
        data = dict(email=self.email, password=self.password)
        auth = AuthService.post("/internal/create", data=data, key="auth", objectify=True)
        self.state.auth = auth

    def compensate(self):
        data = dict(auth=self.state.auth.id)
        AuthService.post("/internal/destroy", data=data)


class CreateTeam(Step):
    def __init__(self, name: str, domain: str, is_open: bool = True):
        self.name = name
        self.domain = domain
        self.is_open = is_open

    def action(self):
        data = dict(name=self.name, domain=self.domain, is_open=self.is_open)
        team = TeamService.create_team(self.state.auth.id, data=data)
        self.state.team = State(id=team.id)

    def compensate(self):
        TeamService.destroy_team(self.state.team.id)


class CreateUser(Step):
    def __init__(self, name: str):
        self.name = name

    def action(self):
        data = dict(team=self.state.team.id, auth=self.state.auth.id, email=self.state.auth.email, name=self.name)
        user = UsersService.post("/internal/create", data=data, key="user", objectify=True)
        self.state.user = user

    def compensate(self):
        data = dict(user=self.state.user.id, team=self.state.team.id)
        UsersService.post("/internal/destroy", data=data)


class CreateBaseChannels(Step):
    def action(self):
        data = dict(team=self.state.team.id, creator=self.state.user.id)
        general_channel = ConversationsService.post(
            "/internal/create",
            data=dict(name="general", is_general=True, **data),
            internal=True,
            key="channel",
            objectify=True,
        )
        random_channel = ConversationsService.post(
            "/internal/create",
            data=dict(name="random", is_random=True, **data),
            internal=True,
            key="channel",
            objectify=True,
        )
        self.state.channels = [general_channel, random_channel]

    def compensate(self):
        for channel in self.state.channels:
            data = dict(team=self.state.team.id, channel=channel.id)
            ConversationsService.post("/internal/destroy", data=data)


class InitTeamSaga(Saga):
    def __init__(
        self,
        email: str = "admin@example.com",
        password: str = "password",
        name: str = "team",
        domain: str = "team.example",
        username: str = "admin",
    ):
        self.steps = [
            CreateAuth(email=email, password=password),
            CreateTeam(name=name, domain=domain, is_open=True),
            CreateUser(name=username),
            CreateBaseChannels(),
        ]

    def on_success(self):
        print("teams.user.joined")
