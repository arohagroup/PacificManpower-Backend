# Generated by Django 4.0.6 on 2023-08-25 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0008_alter_job_post_company_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_post',
            name='job_qualification',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]