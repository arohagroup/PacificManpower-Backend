# Generated by Django 4.0.6 on 2023-04-06 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0034_alter_seeker_profile_createddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seeker_skill_set',
            name='skill_set_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='skill_set', to='spacificmanpower.skill_set'),
        ),
    ]
