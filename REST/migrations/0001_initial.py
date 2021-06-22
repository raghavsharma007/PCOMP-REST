# Generated by Django 3.2.3 on 2021-05-22 14:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('column1', models.CharField(blank=True, max_length=50, null=True)),
                ('column2', models.CharField(blank=True, max_length=50, null=True)),
                ('column3', models.CharField(blank=True, max_length=50, null=True)),
                ('column4', models.CharField(blank=True, max_length=50, null=True)),
                ('column5', models.CharField(blank=True, max_length=50, null=True)),
                ('column6', models.CharField(blank=True, max_length=50, null=True)),
                ('column7', models.CharField(blank=True, max_length=50, null=True)),
                ('column8', models.CharField(blank=True, max_length=50, null=True)),
                ('column9', models.CharField(blank=True, max_length=50, null=True)),
                ('column10', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
