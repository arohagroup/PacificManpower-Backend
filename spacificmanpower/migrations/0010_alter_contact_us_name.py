# Generated by Django 4.0.6 on 2023-04-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0009_alter_subscribe_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_us',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
