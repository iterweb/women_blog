from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

from .models import *


User = get_user_model()


# форма не связанная с моделями
class ContactForm(forms.Form):
    name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-input'}), label='Имя')
    email = forms.EmailField(max_length=250, label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Текст')
    captcha = CaptchaField(label='Каптча')



# форма связанная с моделями
class Add_Post_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выбрать категорию'

    class Meta:
        model = Women
        fields = ['title', 'slug', 'photo', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # пользовательские валидаторы полей формы
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('Длина заголовка должна бить, больше 5 символов')
        elif len(title) > 200:
            raise ValidationError('Длина заголовка не должна бить, больше 200 символов')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 300:
            raise ValidationError('Длина текста должна бить, больше 300 символов')
        return content


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Пароль (ещё раз)', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Комментарий', widget=forms.Textarea(
        attrs={'class': 'form-input', 'id': 'contactcomment', 'rows': 5, 'placeholder': 'Оставьте комментарий здесь'})
    )

    class Meta:
        model = Comment
        fields = ['content']
