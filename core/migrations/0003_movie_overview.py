# Generated by Django 3.2.8 on 2021-10-30 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211030_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='overview',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]