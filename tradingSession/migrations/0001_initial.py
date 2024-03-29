# Generated by Django 2.2.1 on 2019-06-29 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TradingSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomId', models.IntegerField(default=0.0)),
                ('startTime', models.CharField(max_length=255)),
                ('endTime', models.CharField(max_length=255)),
                ('endTimeCount', models.IntegerField()),
                ('userSelectedTraderId', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
