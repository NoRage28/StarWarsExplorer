from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='datasets/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.pk}'
