# Generated by Django 5.0.3 on 2024-03-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='profile_img/', verbose_name='Profile Image'),
        ),
    ]
