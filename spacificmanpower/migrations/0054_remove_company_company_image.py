# Generated by Django 4.0.6 on 2023-04-18 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0053_company_company_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='company_image',
        ),
    ]
