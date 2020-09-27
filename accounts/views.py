import logging
import json

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http.response import JsonResponse

from .forms import LoginForm, RegisterForm, ProfileForm
from tweet_template.forms import RegisterForm as form_template
from accounts.models import CustomUser
from tweet_template.models import TweetTemplate

logger = logging.getLogger(__name__)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('tweet_template:index'))

        context = {
            'form': RegisterForm(),
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")

        # リクエストからフォームを作成
        form = RegisterForm(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'accounts/register.html', {'form': form})

        # 保存する前に一旦取り出す
        user = form.save(commit=False)
        # パスワードをハッシュ化してセット
        user.set_password(form.cleaned_data['password'])
        # ユーザーオブジェクトを保存
        user.save()

        # ログイン処理（取得した Userオブジェクトをセッションに保存 & Userデータを更新）
        auth_login(request, user)

        return redirect(settings.LOGIN_REDIRECT_URL)


register = RegisterView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('tweet_template:index'))

        context = {
            'form': LoginForm(),
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = LoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'accounts/login.html', {'form': form})

        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()

        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)

        # ログイン後処理（ログイン回数を増やしたりする。本来は user_logged_in シグナルを使えばもっと簡単に書ける）
        user.post_login()

        # ロギング
        logger.info("User(id={}) has logged in.".format(user.id))

        # フラッシュメッセージを画面に表示
        messages.info(request, "ログインしました。")

        # ショップ画面にリダイレクト
        return redirect(reverse('tweet_template:index'))


login = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(id={}) has logged out.".format(request.user.id))
            # ログアウト処理
            auth_logout(request)

        return redirect(reverse('tweet_template:index'))

logout = LogoutView.as_view()


class AccountDeleteView(View):
    def get(self, request, *args, **kwargs):
        CustomUser.objects.filter(username=self.request.user).delete()
        auth_logout(self.request)
        return redirect(reverse('tweet_template:index'))

account_delete_view = AccountDeleteView.as_view()


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        screen_id = self.kwargs.get('sid')
        request_user = get_object_or_404(CustomUser, username=screen_id)
        context = {
            'request_user': request_user,
            'templates': request_user.bukuma.all(),
            'form': form_template(),
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストからフォームを作成
        form = form_template(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'tweet_template/create.html', {'form': form})

        form.instance.author = request.user

        # 保存する前に一旦取り出す
        template = form.save(commit=False)
        # ユーザーオブジェクトを保存
        template.save()

        return redirect('accounts:profile', request.user)

profile = ProfileView.as_view()


class SettingsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'accounts/settings.html')
        else:
            return redirect('tweet_template:index')

settings = SettingsView.as_view()


def abukuma(request, pk):
    try:
        template_in_bukuma = request.user.bukuma.get(pk=pk)
        request.user.bukuma.remove(template_in_bukuma)
        data = {'result': 0}
    except ObjectDoesNotExist:
        request.user.bukuma.add(TweetTemplate.objects.get(pk=pk))
        data = {'result': 1}

    return JsonResponse(data)
