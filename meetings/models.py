from django.db import models
from django.conf import settings

class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sinceWhen = models.DateTimeField()
    tilWhen = models.DateTimeField()
    user = models.ForeignKey('auth.User', related_name='meetings', on_delete=models.CASCADE)

    class Meta:
        ordering = ('sinceWhen',)