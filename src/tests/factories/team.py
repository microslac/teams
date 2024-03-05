from factory.django import DjangoModelFactory
from faker import Factory

from teams.models import Team

__all__ = ["TeamFactory"]

fake = Factory.create()


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = fake.company()
    domain = "team@example.com"
