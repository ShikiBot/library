# Generated by Django 3.1.3 on 2020-12-23 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20201111_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'permissions': (('can_add_author', 'can_change_author'),)},
        ),
    ]