# Generated by Django 4.2.11 on 2025-04-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identify_api', '0002_identrequest_status_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='identrequest',
            name='confidence',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
