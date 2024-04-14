# Generated by Django 5.0.4 on 2024-04-13 23:56

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium_care', '0006_aquarium_pincode_alter_fish_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fish',
            name='gender',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='fish',
            name='time_of_birth',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 14, 2, 56, 57, 67257)),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='gender',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='shrimp',
            name='time_of_birth',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 14, 2, 56, 57, 67257)),
        ),
        migrations.AlterField(
            model_name='snail',
            name='gender',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='snail',
            name='time_of_birth',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 14, 2, 56, 57, 67257)),
        ),
        migrations.CreateModel(
            name='Fugue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satiety', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100)])),
                ('is_alive', models.BooleanField(default=True)),
                ('gender', models.BooleanField(default=True)),
                ('time_of_birth', models.DateTimeField(default=datetime.datetime(2024, 4, 14, 2, 56, 57, 67257))),
                ('time_of_sell', models.DateTimeField(blank=True, null=True)),
                ('time_of_breeding', models.DateTimeField(blank=True, null=True)),
                ('is_sold', models.BooleanField(default=False)),
                ('cost', models.IntegerField(default=0)),
                ('aquarium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium_care.aquarium')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
