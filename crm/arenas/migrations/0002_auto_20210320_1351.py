# Generated by Django 3.1.4 on 2021-03-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arenas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arena',
            name='identifier',
            field=models.CharField(max_length=125, unique=True),
        ),
    ]
