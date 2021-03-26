# Generated by Django 3.0.2 on 2021-03-26 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumption',
            name='id',
        ),
        migrations.AlterField(
            model_name='consumption',
            name='meter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.Meter'),
        ),
    ]