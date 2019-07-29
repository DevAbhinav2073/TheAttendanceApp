from django.db import models

# Create your models here.
from apps.constants import BATCH_CHOICES


class Programme(models.Model):
    name = models.CharField(max_length=50)
    short_form = models.CharField(max_length=5,
                                  help_text='This is the abbreviated form that is used in roll number. For example BCT for Computer Engineering')

    def __str__(self):
        return self.name


class Notice(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    batch = models.CharField(max_length=4, choices=BATCH_CHOICES)
    message = models.CharField(max_length=120)
    send_sms = models.BooleanField(default=False)
    send_email = models.BooleanField(default=True)

    def __str__(self):
        return self.message
