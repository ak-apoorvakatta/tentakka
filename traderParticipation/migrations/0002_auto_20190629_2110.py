# Generated by Django 2.2.1 on 2019-06-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traderParticipation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='traderparticapation',
            name='expectancy',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='maxDD',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='mean',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='odds_of_win',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='predicted_return',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='sharpe',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='sortino',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='traderparticapation',
            name='std',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='traderparticapation',
            name='roomId',
            field=models.IntegerField(default=0.0),
        ),
    ]