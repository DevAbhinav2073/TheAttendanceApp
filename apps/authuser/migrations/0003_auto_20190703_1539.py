# Generated by Django 2.2.2 on 2019-07-03 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0002_auto_20190703_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Teacher', max_length=10),
        ),
    ]
