# Generated by Django 4.0.6 on 2023-04-28 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0003_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_post_activity',
            name='userstatus',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
