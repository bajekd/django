# Generated by Django 3.2.3 on 2021-06-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_project_long_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='long_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]