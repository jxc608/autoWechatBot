# Generated by Django 2.1.1 on 2018-09-08 01:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('DServerAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clubs',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('expiredTime', models.DateTimeField(verbose_name='expired Time')),
            ],
        ),
        migrations.CreateModel(
            name='GameID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_nick_name', models.CharField(max_length=200)),
                ('gameid', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wechat_id', models.CharField(max_length=200)),
                ('wechat_nick_name', models.CharField(max_length=50)),
                ('current_Score', models.CharField(max_length=20)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DServerAPP.Clubs')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(verbose_name='create time')),
                ('room_id', models.CharField(max_length=20)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DServerAPP.Player')),
            ],
        ),
        migrations.AddField(
            model_name='gameid',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DServerAPP.Player'),
        ),
    ]
