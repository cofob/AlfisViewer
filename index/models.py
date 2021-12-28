import time
from django.db import models
from secrets import token_hex
import traceback


def gen_id():
    return token_hex(4).upper()


class Error(models.Model):
    id = models.CharField(primary_key=True, default=gen_id, max_length=64)
    exception = models.TextField()
    timestamp = models.IntegerField(default=time.time)

    @staticmethod
    def submit(exc):
        e = Error(exception=''.join(traceback.format_exception(exc)))
        e.save()
        return e.id

    def __str__(self):
        return self.id
