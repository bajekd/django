# Generated by Django 3.1.7 on 2021-03-23 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0008_auto_20210323_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='owner',
        ),
    ]
