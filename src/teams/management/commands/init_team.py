from micro.jango.commands import BaseCommand
from teams.sagas.init_team import InitTeamSaga


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        email, password = "admin@example.com", "password"
        saga = InitTeamSaga(email=email, password=password)
        saga.run()
        if saga.is_success:
            team, auth, user = saga.state.team.id, saga.state.auth.id, saga.state.user.id
            self.stdout.write(f"Team: {team} (demo: {False}) \n"
                              f"Email: {email} - Password: {password} \n"
                              f"Auth: {auth} - User: {user}")
