# Generated by Django 4.2.11 on 2025-04-04 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_profile_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
