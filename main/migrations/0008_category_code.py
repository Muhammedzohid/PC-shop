# Generated by Django 5.0.6 on 2024-05-17 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_refund_options_alter_sellproduct_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='code',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
