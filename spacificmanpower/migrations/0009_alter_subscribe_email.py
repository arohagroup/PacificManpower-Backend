# Generated by Django 4.0.6 on 2023-04-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0008_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='email',
            field=models.CharField(max_length=25),
        ),
    ]
