from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.validators import MaxLengthValidator
from django_cryptography.fields import encrypt

User._meta.get_field('email')._unique = True     # adding Unique constrain to email in User model


# Create your models here.
class Daily(models.Model):
    date = models.DateField(null=False)
    content = encrypt(RichTextField(null=False, validators=[MaxLengthValidator(30000)]))
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    bookmark = models.BooleanField(default=False)

    class Meta:
        unique_together = (('date', 'user'),)

    def __str__(self):
        return f"{self.user} - {str(self.date)}"

    def get_absolute_url(self):
        return reverse('view_specific_content', kwargs={'date': self.date})


class Feedback(models.Model):
    subject = models.CharField(max_length=100)
    your_feedback = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.subject}'
