# Generated by Django 4.0.6 on 2023-04-26 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='business_stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_stream_name', models.CharField(max_length=100)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('profile_description', models.CharField(max_length=1000)),
                ('establishment_date', models.DateField()),
                ('company_website_url', models.CharField(max_length=500)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('business_stream_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business_stream_id', to='spacificmanpower.business_stream')),
            ],
        ),
        migrations.CreateModel(
            name='experince_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experince_type', models.CharField(max_length=20)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='job_location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='job_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_company_name_hidden', models.BooleanField()),
                ('job_title', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('job_description', models.CharField(max_length=500)),
                ('salary', models.IntegerField(blank=True, max_length=30, null=True)),
                ('is_active', models.BooleanField()),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('company_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_id', to='spacificmanpower.company')),
                ('experince_type_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experince_type_id', to='spacificmanpower.experince_type')),
                ('job_location_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_location_id', to='spacificmanpower.job_location')),
            ],
        ),
        migrations.CreateModel(
            name='job_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(max_length=20)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='skill_set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_set_name', models.CharField(max_length=200)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=122)),
                ('last_name', models.CharField(max_length=122)),
                ('email_address', models.CharField(max_length=122, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('isactive', models.BooleanField(blank=True)),
                ('contact_number', models.IntegerField()),
                ('email_notification_active', models.BooleanField()),
                ('user_image', models.ImageField(blank=True, max_length=200, upload_to='')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type_name', models.CharField(max_length=20)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='seeker_profile',
            fields=[
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_account_idss', serialize=False, to='spacificmanpower.user_account')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('current_salary', models.IntegerField(blank=True, null=True)),
                ('is_annually_monthly', models.CharField(blank=True, max_length=100)),
                ('currency', models.CharField(blank=True, max_length=50)),
                ('uploaded_cv', models.FileField(blank=True, null=True, upload_to='')),
                ('createdDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_log',
            fields=[
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_account_id', serialize=False, to='spacificmanpower.user_account')),
                ('last_login_date', models.DateTimeField(auto_now=True)),
                ('last_job_apply_date', models.DateTimeField(blank=True, null=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='user_account',
            name='user_type_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='usertype', to='spacificmanpower.user_type'),
        ),
        migrations.CreateModel(
            name='trending_news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=100)),
                ('news_description', models.CharField(max_length=50)),
                ('news_image', models.ImageField(blank=True, max_length=200, null=True, upload_to='')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_id_trending_news', to='spacificmanpower.user_account')),
            ],
        ),
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
        migrations.CreateModel(
            name='seeker_skill_set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.IntegerField()),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('skill_set_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='skill_set_id_seeker', to='spacificmanpower.skill_set')),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_idsss', to='spacificmanpower.user_account')),
            ],
        ),
        migrations.CreateModel(
            name='job_post_skill_set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.IntegerField()),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('job_post_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_post_id_job_post_skill_set', to='spacificmanpower.job_post')),
                ('skill_set_id', models.ForeignKey(blank=True, default=None, max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skill_set_id', to='spacificmanpower.skill_set')),
            ],
        ),
        migrations.CreateModel(
            name='job_post_activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('job_post_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_post_id', to='spacificmanpower.job_post')),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_idssss', to='spacificmanpower.user_account')),
            ],
        ),
        migrations.AddField(
            model_name='job_post',
            name='job_type_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_type_id', to='spacificmanpower.job_type'),
        ),
        migrations.AddField(
            model_name='job_post',
            name='posted_by_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posted_by_id', to='spacificmanpower.job_post_activity'),
        ),
        migrations.CreateModel(
            name='experience_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_current_job', models.BooleanField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('job_location_city', models.CharField(blank=True, max_length=50, null=True)),
                ('job_location_state', models.CharField(blank=True, max_length=50, null=True)),
                ('job_location_country', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_ids', to='spacificmanpower.user_account')),
            ],
        ),
        migrations.CreateModel(
            name='education_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_degree_name', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=50)),
                ('institute_university_name', models.CharField(max_length=100)),
                ('starting_date', models.DateTimeField()),
                ('completion_date', models.DateTimeField()),
                ('percentage', models.IntegerField(blank=True, null=True)),
                ('cgpa', models.IntegerField(blank=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_id_education_detail', to='spacificmanpower.user_account')),
            ],
        ),
        migrations.CreateModel(
            name='contact_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=15)),
                ('message', models.CharField(max_length=400)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('user_account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_account_id_contact_us', to='spacificmanpower.user_account')),
            ],
        ),
        migrations.CreateModel(
            name='company_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyimage', models.ImageField(blank=True, max_length=200, upload_to='')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('company_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_id_company_image', to='spacificmanpower.company')),
            ],
        ),
    ]
