import validators
from micro.jango.serializers import BaseModelSerializer, TimestampField
from rest_framework import serializers

from teams.models import Team


class TeamSerializer(BaseModelSerializer):
    creator = serializers.CharField(required=True, write_only=True)
    is_open = serializers.BooleanField(required=False, default=False)
    created = TimestampField(required=False, read_only=True)
    updated = TimestampField(required=False, read_only=True)
    updater = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "domain", "is_open", "created", "creator", "updated", "updater")
        read_only_fields = ("created", "updated")

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError("Invalid domain")
        return value

    def to_representation(self, instance: Team):
        data = super().to_representation(instance)
        data.update(creator=instance.creator_id)
        data.update(updater=instance.updater_id)
        data = {k: v for k, v in data.items() if v is not None}
        return data
