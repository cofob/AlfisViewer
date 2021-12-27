from django.db import models
from domain.models import Domain


class Block(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    hash = models.BinaryField(max_length=64)
