# Generated by Django 3.0.3 on 2020-09-26 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_template', '0002_auto_20200926_1358'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bukuma',
            field=models.ManyToManyField(blank=True, to='tweet_template.TweetTemplate', verbose_name='ブクマ'),
        ),
    ]
