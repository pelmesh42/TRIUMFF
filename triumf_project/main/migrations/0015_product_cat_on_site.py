# Generated by Django 3.2.20 on 2023-08-16 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_town_order_adress'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='CAT_on_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category'),
        ),
    ]
