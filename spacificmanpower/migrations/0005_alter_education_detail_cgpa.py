# Generated by Django 4.0.6 on 2023-05-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0004_alter_education_detail_cgpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education_detail',
            name='cgpa',
            field=models.IntegerField(blank=True),
        ),
    ]
