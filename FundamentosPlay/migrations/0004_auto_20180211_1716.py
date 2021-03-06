# Generated by Django 2.0 on 2018-02-11 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FundamentosPlay', '0003_auto_20180211_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='id',
        ),
        migrations.AddField(
            model_name='player',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FundamentosPlay.LeaderBoard'),
        ),
        migrations.AlterField(
            model_name='player',
            name='nombre',
            field=models.CharField(default='Nombres y Apellidos', max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='unidad',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
