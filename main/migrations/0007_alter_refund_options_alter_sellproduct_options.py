# Generated by Django 5.0.6 on 2024-05-17 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_enterproduct_code_sellproduct_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='refund',
            options={'ordering': ['-refunded_at']},
        ),
        migrations.AlterModelOptions(
            name='sellproduct',
            options={'ordering': ['-sold_at']},
        ),
    ]
