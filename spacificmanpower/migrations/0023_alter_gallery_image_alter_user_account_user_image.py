# Generated by Django 4.0.6 on 2024-05-02 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0022_alter_company_company_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='gallery/'),
        ),
        migrations.AlterField(
            model_name='user_account',
            name='user_image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='user/'),
        ),
    ]
