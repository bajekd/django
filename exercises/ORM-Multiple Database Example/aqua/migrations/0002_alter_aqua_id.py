# Generated by Django 3.2 on 2021-04-30 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aqua', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aqua',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
