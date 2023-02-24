# Generated by Django 4.1.7 on 2023-02-24 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fastrack_web', '0005_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='inventories',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='fastrack_web.inventory'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('P', 'Placed'), ('K', 'In Kitchen'), ('R', 'Ready'), ('D', 'Delivered')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='wait_time',
            field=models.TimeField(null=True),
        ),
    ]
