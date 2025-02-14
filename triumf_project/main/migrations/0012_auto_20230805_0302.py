# Generated by Django 3.2.20 on 2023-08-04 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_customuser_is_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='email', max_length=254),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default='+700000000', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='town',
            field=models.CharField(default='адрес доставки', max_length=200),
        ),
    ]
