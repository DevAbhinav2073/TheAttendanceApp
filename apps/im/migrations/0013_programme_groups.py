# Generated by Django 2.2.2 on 2019-08-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('im', '0012_auto_20190803_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='groups',
            field=models.CharField(default='A, B', help_text='Enter groups separated by commas', max_length=50),
        ),
    ]