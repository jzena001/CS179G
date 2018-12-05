# Generated by Django 2.1.3 on 2018-12-04 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo', models.CharField(max_length=6)),
                ('hashtag', models.CharField(max_length=280, null=True)),
                ('tweetkey', models.DecimalField(decimal_places=0, max_digits=19)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('mention', models.CharField(max_length=280, null=True)),
                ('tweet', models.CharField(max_length=1024)),
                ('time_stamp', models.DateTimeField(verbose_name='date posted')),
                ('user_name', models.CharField(max_length=280)),
                ('sentiment', models.DecimalField(decimal_places=0, max_digits=1)),
            ],
        ),
    ]
