# Generated by Django 3.2.20 on 2023-07-24 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_customuser_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Название', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Название', max_length=200)),
                ('desc', models.TextField(blank=True, verbose_name='Сжатое описание')),
                ('full_desc', models.TextField(blank=True, verbose_name='Полное описание')),
                ('COMPOSITION', models.TextField(blank=True, verbose_name='СОСТАВ И УХОД')),
                ('MEASUREMENTS', models.TextField(blank=True, verbose_name='ОБМЕРЫ')),
                ('image', models.ImageField(blank=True, upload_to='static\\media\\img')),
                ('amount', models.IntegerField(default='0')),
                ('price', models.IntegerField(default='10000')),
                ('discount', models.BooleanField(default=False, verbose_name='есть скидка')),
                ('old_price', models.IntegerField(default='999', verbose_name='старая цена')),
                ('my_id', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='adress',
            field=models.CharField(blank=True, default='Adress', max_length=200),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+70000000000', max_length=128, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='rev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prons', models.TextField(blank=True, verbose_name='Плюсы')),
                ('cons', models.TextField(blank=True, verbose_name='Минусы')),
                ('body', models.TextField(blank=True, verbose_name='Комментарий')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rev_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Имя клиента', max_length=200)),
                ('sername', models.CharField(default='Фамилия клиента', max_length=200)),
                ('town', models.CharField(default='город клиента', max_length=200)),
                ('comment', models.TextField(blank=True, verbose_name='Коментарий')),
                ('sp_code', models.CharField(blank=True, max_length=16)),
                ('products', models.ManyToManyField(to='main.product')),
                ('users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Categoryhasitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorys', models.ForeignKey(db_column='category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category')),
                ('products', models.ForeignKey(db_column='product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.product')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, through='main.Categoryhasitem', to='main.product'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='basket',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_that_basket', to='main.product'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='like',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_that_like', to='main.product'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='was_basket',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_that_was_basket', to='main.product'),
        ),
    ]
