# Generated by Django 3.0.3 on 2020-09-26 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet_template', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweettemplate',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tweettemplate',
            name='hashtag',
            field=models.ManyToManyField(blank=True, to='tweet_template.Hashtag', verbose_name='ハッシュタグ'),
        ),
    ]