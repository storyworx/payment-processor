from django.db import models


class KafkaState(models.Model):
    partition = models.IntegerField(blank=False, null=False, default=0)
    offset = models.IntegerField(blank=False, null=False)
    topic = models.CharField(max_length=255)
    source_id = models.IntegerField(blank=False, null=False)
