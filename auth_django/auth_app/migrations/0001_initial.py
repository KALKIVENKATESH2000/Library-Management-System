# Generated by Django 4.0.4 on 2022-06-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('published', models.BooleanField(default=False)),
                ('bookcount', models.IntegerField(null=True)),
            ],
        ),
    ]