from django.db import models

# Create your models here.
class Runner(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, null=False, blank=False)
    name = models.CharField(max_length=30, null=False, blank=False)
    lastContacted = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=50, null=False, blank=False)
    port = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=30, null=False, blank=False)


class Workspace(models.Model):
    id = models.CharField(primary_key=True, max_length=50, null=False, blank=False)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE, null=False, blank=False)
    environment = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=30, null=False, blank=False)
    port = models.IntegerField(null=False, blank=False)


