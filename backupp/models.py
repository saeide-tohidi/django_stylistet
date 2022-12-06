from django.db import models

# Create your models here.


class BackupHistory(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
