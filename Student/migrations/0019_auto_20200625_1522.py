# Generated by Django 2.2.13 on 2020-06-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_auto_20200625_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='room',
            field=models.CharField(max_length=10, null=True),
        ),
    ]