# Generated by Django 3.2 on 2022-05-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=17)),
                ('author', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, default='')),
                ('publish', models.CharField(max_length=200)),
                ('publishyear', models.CharField(max_length=200)),
                ('time', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=False)),
                ('borrower', models.CharField(blank=True, default='', max_length=200)),
                ('burl', models.CharField(max_length=100)),
                ('bhit', models.IntegerField(default=0)),
            ],
        ),
    ]
