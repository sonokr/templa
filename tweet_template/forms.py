from django import forms

from .models import TweetTemplate


class RegisterForm(forms.ModelForm):
    """テンプレート登録用のフォーム"""

    class Meta:
        model = TweetTemplate
        fields = ('name',
                  'content',)

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'テンプレート名'}),
            'content': forms.Textarea(attrs={'placeholder': 'ツイートテンプレート'}),
        }
