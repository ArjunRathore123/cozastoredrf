# Generated by Django 4.2.10 on 2024-02-16 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('seller', 'Seller'), ('buyer', 'Buyer'), ('admin', 'Admin')], max_length=10),
        ),
    ]