# Generated by Django 4.0.6 on 2023-08-26 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0018_alter_job_post_job_qualification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='job_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]