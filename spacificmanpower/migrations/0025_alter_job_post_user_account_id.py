# Generated by Django 4.0.6 on 2024-05-02 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0024_alter_job_post_job_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='user_account_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_id_job_post', to='spacificmanpower.user_account'),
        ),
    ]