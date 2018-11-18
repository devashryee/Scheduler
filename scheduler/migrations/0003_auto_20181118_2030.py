# Generated by Django 2.1.3 on 2018-11-18 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_remove_timeslot_rname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='cname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='times', to='scheduler.Course'),
        ),
    ]
