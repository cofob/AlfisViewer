from django.db import models


class Domain(models.Model):
    hash = models.CharField(max_length=64)
    real_domain = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.real_domain if self.real_domain else self.hash
