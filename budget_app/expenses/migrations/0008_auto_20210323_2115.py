# Generated by Django 3.1.7 on 2021-03-23 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0007_category_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='user',
            new_name='owner',
        ),
    ]
