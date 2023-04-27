# Generated by Django 4.0.6 on 2023-04-27 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spacificmanpower', '0002_delete_subscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=25)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_id_subscribe', to='spacificmanpower.user_account')),
            ],
        ),
    ]