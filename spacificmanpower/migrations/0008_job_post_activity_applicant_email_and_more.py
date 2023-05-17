# Generated by Django 4.0.6 on 2023-05-17 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0007_gallery_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_post_activity',
            name='applicant_email',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job_post_activity',
            name='applicant_name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job_post_activity',
            name='expected_pay',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job_post_activity',
            name='experience',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experince_type_job_post_activity', to='spacificmanpower.experince_type'),
        ),
        migrations.AddField(
            model_name='job_post_activity',
            name='notice_period',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='job_post_activity',
            name='phone_num',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job_post_activity',
            name='uploaded_cv',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]