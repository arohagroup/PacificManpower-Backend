# Generated by Django 4.0.6 on 2023-04-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0015_alter_seeker_profile_current_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seeker_profile',
            name='current_salary',
            field=models.IntegerField(),
        ),
    ]
