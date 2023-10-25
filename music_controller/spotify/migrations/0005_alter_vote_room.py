# Generated by Django 3.2.3 on 2021-05-20 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_room_current_song'),
        ('spotify', '0004_alter_vote_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.room', verbose_name='Forein key to room'),
        ),
    ]
