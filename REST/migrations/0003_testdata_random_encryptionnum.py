# Generated by Django 3.2.3 on 2021-06-08 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0002_auto_20210601_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='testdata',
            name='random_encryptionNum',
            field=models.IntegerField(default=0),
        ),
    ]