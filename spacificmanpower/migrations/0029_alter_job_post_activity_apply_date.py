# Generated by Django 4.0.6 on 2023-04-06 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0028_alter_job_post_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post_activity',
            name='apply_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
