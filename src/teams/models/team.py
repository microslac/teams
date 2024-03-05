from django.db import models
from micro.jango.models import DeletedModel, HistoryModel, UUIDModel
from micro.jango.models.fields import ShortIdField


class Team(UUIDModel, DeletedModel, HistoryModel):
    id = ShortIdField(prefix="T", primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    domain = models.CharField(max_length=255, blank=False, unique=True, null=False)
    is_open = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = "teams"
