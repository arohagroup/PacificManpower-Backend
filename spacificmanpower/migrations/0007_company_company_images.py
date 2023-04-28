# Generated by Django 4.0.6 on 2023-04-28 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0006_remove_company_company_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_images',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_id_company', to='spacificmanpower.company_image'),
        ),
    ]
