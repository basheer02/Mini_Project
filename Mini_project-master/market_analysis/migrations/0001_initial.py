# Generated by Django 4.1.5 on 2023-06-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=20)),
                ('count', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'gender_data',
                'managed': False,
            },
        ),
    ]
