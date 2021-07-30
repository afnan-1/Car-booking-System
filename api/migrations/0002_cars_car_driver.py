# Generated by Django 3.2.5 on 2021-07-30 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='car_driver',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='car_driver', to='api.driver'),
            preserve_default=False,
        ),
    ]
