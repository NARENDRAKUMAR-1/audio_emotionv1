# Generated by Django 4.0.5 on 2022-06-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio_store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.FileField(upload_to='documents/')),
            ],
            options={
                'db_table': 'Audio_store',
            },
        ),
    ]
