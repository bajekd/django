# Generated by Django 3.2.3 on 2021-05-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=75, verbose_name='From what website given item was scraped')),
                ('link', models.TextField(verbose_name='Link to item')),
                ('title', models.CharField(max_length=50, verbose_name='Title of item')),
                ('publish_date', models.DateField(verbose_name='Date when item was published')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateField(auto_now=True, verbose_name='Updated at')),
            ],
        ),
    ]
