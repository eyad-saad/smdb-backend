# Generated by Django 3.2.8 on 2021-10-31 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20211031_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
