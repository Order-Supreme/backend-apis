# Generated by Django 4.1.7 on 2023-03-07 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fastrack_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='fastrack_web.imagemodel'),
        ),
    ]
