# Generated by Django 5.0.6 on 2024-06-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=13)),
            ],
        ),
    ]