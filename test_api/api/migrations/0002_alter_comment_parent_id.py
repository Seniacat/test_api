# Generated by Django 3.2.8 on 2022-04-25 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Родительский комментарий'),
        ),
    ]