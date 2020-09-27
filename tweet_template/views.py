from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import View, ListView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q

import operator
from functools import reduce

from .models import TweetTemplate, Hashtag
from .forms import RegisterForm

from accounts.models import CustomUser


class TweetTemplateListView(View):
    def get(self, request, *args, **kwargs):
        queryset = TweetTemplate.objects.all()
        context = {
            'templates': queryset,
            'form': RegisterForm(),
        }
        return render(request, 'tweet_template/index.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストからフォームを作成
        form = RegisterForm(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'tweet_template/create.html', {'form': form})

        form.instance.author = request.user

        ht_list = self.request.POST.get('hashtag', None).split()

        # 保存する前に一旦取り出す
        template = form.save(commit=False)

        # ユーザーオブジェクトを保存
        template.save()

        for ht in ht_list:
            try:
                the_tag = Hashtag.objects.get(name=ht)
                template.hashtag.add(the_tag)
            except ObjectDoesNotExist:
                new_tag = Hashtag(name=ht)
                new_tag.save()
                template.hashtag.add(new_tag)

        return redirect('tweet_template:index')

index = TweetTemplateListView.as_view()


def delete_template(request, pk):
    TweetTemplate.objects.filter(pk=pk).delete()
    return redirect('accounts:profile')


class Explore(View):
    def get(self, request, *args, **kwargs): 
        return render(request, 'tweet_template/explore.html')

explore = Explore.as_view()


class Search(View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('query'): 
            q_word = self.request.GET.get('query').split()

            queryset = TweetTemplate.objects.filter(
                reduce(operator.and_, (Q(name__icontains=q) for q in q_word)) |
                reduce(operator.and_, (Q(content__icontains=q) for q in q_word)) |
                reduce(operator.or_, (Q(hashtag__name=q) for q in q_word))
            ).distinct()

            context = {
                'q_word': q_word,
                'object_list': queryset
            }

            return render(request, 'tweet_template/search_result.html', context)
        else:
            return render(request, 'tweet_template/search_result.html')

search = Search.as_view()
