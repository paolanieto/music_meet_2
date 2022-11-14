# Generated by Django 4.1.1 on 2022-11-14 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_user_group_account_user_musician_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='instruments_needed',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='group_Account',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='musician_Account',
            field=models.BooleanField(default=False),
        ),
    ]
