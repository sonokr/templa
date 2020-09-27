from django.core.management.base import BaseCommand
from tweet_template.models import TweetTemplate


class Command(BaseCommand):
    def handle(self, *args, **options):
        for tt in TweetTemplate.objects.all():
            tt.rank = tt.customuser_set.count()
            tt.save()
