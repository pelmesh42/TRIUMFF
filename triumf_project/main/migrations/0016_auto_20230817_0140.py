# Generated by Django 3.2.20 on 2023-08-16 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_product_cat_on_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='extra_image1',
            field=models.ImageField(blank=True, upload_to='static\\media\\img'),
        ),
        migrations.AddField(
            model_name='product',
            name='extra_image2',
            field=models.ImageField(blank=True, upload_to='static\\media\\img'),
        ),
        migrations.AddField(
            model_name='product',
            name='extra_image3',
            field=models.ImageField(blank=True, upload_to='static\\media\\img'),
        ),
        migrations.AddField(
            model_name='product',
            name='extra_image4',
            field=models.ImageField(blank=True, upload_to='static\\media\\img'),
        ),
    ]
