from django.db import models
from django.utils import timezone


class TweetTemplate(models.Model):
    """ツイートテンプレートモデル"""

    class Meta(object):
        db_table = "tweet_template"

    name = models.CharField(verbose_name="テンプレート名", max_length=255)

    content = models.TextField(verbose_name="本文", max_length=1000, blank=True)

    create_date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="author",
        blank=True,
        null=True,
    )

    rank = models.IntegerField(verbose_name="順位", null=False, default=-1)

    hashtag = models.ManyToManyField(
        "tweet_template.Hashtag", verbose_name="ハッシュタグ", blank=True,
    )

    def __str__(self):
        return self.name


class Hashtag(models.Model):
    class Meta(object):
        db_table = "hashtag"

    name = models.CharField(verbose_name="タグ名", max_length=100, null=True, blank=True)

