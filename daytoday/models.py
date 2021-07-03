from django.db import models
from django.utils import timezone


# Create your models here.
class Daily(models.Model):
    date = models.DateField(null=False)
    content = models.CharField(max_length=30000, null=False)
    created_date = models.DateTimeField(timezone.now())
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date)
