from django.db import models


# Create your models here.


class Programme(models.Model):
    name = models.CharField(max_length=50)
    short_form = models.CharField(max_length=5,
                                  help_text='This is the abbreviated form that is used in roll number. For example BCT for Computer Engineering')

    def __str__(self):
        return self.name
