# Generated by Django 2.2 on 2019-04-07 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20190407_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ('sinceWhen',)},
        ),
    ]