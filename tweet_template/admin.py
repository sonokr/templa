from django.contrib import admin

from .models import TweetTemplate, Hashtag


admin.site.register(TweetTemplate)
admin.site.register(Hashtag)
