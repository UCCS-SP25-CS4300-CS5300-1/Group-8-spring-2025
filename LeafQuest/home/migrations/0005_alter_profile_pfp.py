# Generated by Django 4.2.11 on 2025-03-14 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_friendrequest_friendlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pfp',
            field=models.ImageField(blank=True, default='profile/default/profile.png', upload_to='profile/'),
        ),
    ]
