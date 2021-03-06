# Generated by Django 3.2.5 on 2021-08-02 20:05

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesskey',
            name='key',
            field=models.CharField(max_length=100, validators=[accounts.models.validate_dummy]),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='image',
            field=models.CharField(max_length=100, validators=[accounts.models.validate_dummy]),
        ),
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.CharField(max_length=100, validators=[accounts.models.validate_dummy]),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, validators=[accounts.models.validate_dummy]),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]
