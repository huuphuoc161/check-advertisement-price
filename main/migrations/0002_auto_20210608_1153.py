# Generated by Django 3.1.7 on 2021-06-08 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanpham',
            name='TenSP',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]