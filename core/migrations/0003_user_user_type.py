# Generated by Django 4.1.7 on 2023-02-23 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('R', 'Restaurant'), ('C', 'Customer')], default=('C', 'Customer'), max_length=50),
        ),
    ]