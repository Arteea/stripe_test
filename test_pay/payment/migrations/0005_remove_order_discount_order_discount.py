# Generated by Django 5.1.6 on 2025-03-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_discount_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ManyToManyField(blank=True, null=True, to='payment.discount', verbose_name='Скидка'),
        ),
    ]
