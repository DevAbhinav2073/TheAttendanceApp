# Generated by Django 2.2.2 on 2019-06-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('im', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='practical_full_marks',
            field=models.IntegerField(default=0, help_text='Full marks of theory'),
        ),
        migrations.AddField(
            model_name='subject',
            name='theory_full_marks',
            field=models.IntegerField(default=0, help_text='Full marks of theory'),
        ),
        migrations.DeleteModel(
            name='SubjectFullAndPassMark',
        ),
    ]
