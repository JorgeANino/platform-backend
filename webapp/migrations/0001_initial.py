# Generated by Django 3.2.10 on 2023-10-09 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('category', models.CharField(choices=[
                 ('Electronics', 'Electronics'), ('Clothing', 'Clothing'), ('Food', 'Food')], max_length=255)),
            ],
        ),
    ]
