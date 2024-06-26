# Generated by Django 5.0.3 on 2024-03-28 03:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_delete_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, null=True, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_img', models.ImageField(blank=True, default='user.png', null=True, upload_to='profile_img/')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
