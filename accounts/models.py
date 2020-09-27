from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta(object):
        db_table = "custom_user"

    login_count = models.IntegerField(verbose_name="ログイン回数", default=0)

    description = models.TextField(verbose_name="自己紹介", max_length=400, null=True)
    icon_url = models.CharField(verbose_name="アイコンURL", max_length=200, null=True)
    bg_url = models.CharField(verbose_name="背景URL", max_length=200, null=True)

    bukuma = models.ManyToManyField(
        "tweet_template.TweetTemplate", verbose_name="ブクマ", blank=True,
    )

    def post_login(self):
        """ログイン後処理"""
        # ログイン回数を増やす
        self.login_count += 1
        self.save()
