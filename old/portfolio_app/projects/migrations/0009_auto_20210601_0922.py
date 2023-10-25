# Generated by Django 3.2.3 on 2021-06-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_gif'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='description',
            new_name='long_description',
        ),
        migrations.AddField(
            model_name='project',
            name='short_description',
            field=models.CharField(default='TBA', max_length=256),
            preserve_default=False,
        ),
    ]