# Generated by Django 2.1.1 on 2018-10-02 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DServerAPP', '0010_auto_20180924_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='historygame',
            name='master_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historygame',
            name='player_data',
            field=models.CharField(default='none', max_length=1000),
        ),
    ]
