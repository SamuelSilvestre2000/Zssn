# Generated by Django 4.2 on 2023-04-26 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('points', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Survivor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('last_location_latitude', models.FloatField()),
                ('last_location_longitude', models.FloatField()),
                ('infected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SurvivorInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item')),
                ('survivor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.survivor')),
            ],
        ),
        migrations.AddField(
            model_name='survivor',
            name='inventory',
            field=models.ManyToManyField(through='api.SurvivorInventory', to='api.item'),
        ),
    ]
