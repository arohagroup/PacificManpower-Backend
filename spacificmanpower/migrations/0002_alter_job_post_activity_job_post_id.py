# Generated by Django 4.0.6 on 2023-05-19 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post_activity',
            name='job_post_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_post_id', to='spacificmanpower.job_post'),
        ),
    ]
