# Generated by Django 4.0.6 on 2024-03-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0019_alter_job_post_job_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post_activity',
            name='phone_num',
            field=models.CharField(max_length=22),
        ),
        migrations.AlterField(
            model_name='user_account',
            name='contact_number',
            field=models.CharField(max_length=22),
        ),
    ]
