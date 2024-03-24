from micro.patterns.saga import Step, State, Saga
from micro.services.registry import AuthService, UsersService, ConversationsService
from teams.services import TeamService


class CreateAuth(Step):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def action(self):
        data = dict(email=self.email, password=self.password)
        auth = AuthService.post("/internal/create", data=data, key="auth")
        self.state.auth = State(id=auth.pop("id"))

    def compensate(self):
        data = dict(id=self.state.auth.id)
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
        data = dict(team=self.state.team.id, auth=self.state.auth.id, name=self.name)
        user = UsersService.post("/internal/create", data=data, key="user")
        self.state.user = State(id=user.pop("id"))

    def compensate(self):
        data = dict(id=self.state.user.id)
        UsersService.post("/internal/destroy", data=data)


class CreateBaseChannels(Step):
    def action(self):
        data = dict(team=self.state.team.id, creator=self.state.user.id)
        general_channel = ConversationsService.post(
            "/internal/create",
            data=dict(name="general", is_general=True, **data),
            internal=True,
            key="channel"
        )
        random_channel = ConversationsService.post(
            "/internal/create",
            data=dict(name="random", is_random=True, **data),
            internal=True,
            key="channel"
        )
        self.state.channel_ids = [general_channel.pop("id"), random_channel.pop("id")]

    def compensate(self):
        for channel_id in self.state.channel_ids:
            data = dict(team=self.state.team.id, id=channel_id)
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
