# Generated by Django 2.2.11 on 2020-07-09 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0026_gatepass_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatepass',
            name='left_gate',
            field=models.BooleanField(default=False),
        ),
    ]