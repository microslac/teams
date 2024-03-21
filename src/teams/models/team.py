from core.models import DeletedModel, HistoryModel, UUIDModel
from core.models.fields import ShortIdField
from django.db import models


class Team(UUIDModel, DeletedModel, HistoryModel):
    id = ShortIdField(prefix="T", primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    domain = models.CharField(max_length=255, blank=False, unique=True, null=False)
    is_open = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = "teams"
