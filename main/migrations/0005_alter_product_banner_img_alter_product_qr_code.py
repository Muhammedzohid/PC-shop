# Generated by Django 5.0.6 on 2024-05-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_qty_enterproduct_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='banner_img',
            field=models.ImageField(upload_to='media/banner-img/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='media/qr'),
        ),
    ]
