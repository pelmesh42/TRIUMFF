from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm , TextInput , EmailInput , FileInput , ModelForm
from .models import CustomUser , product , rev , order


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username",)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class rev_f(ModelForm):
    class Meta:
        model = rev
        fields = ['prons','cons' , 'body']
        widgets = {
            "prons": TextInput (attrs = { 'placeholder': 'prons'}),
            "cons": TextInput (attrs = { 'placeholder': 'cons'}),
            "body": TextInput (attrs = { 'placeholder': 'main'}),
            }


class order_f(ModelForm):
    class Meta:
        model = order
        fields = ['adress', 'name' , 'sername' , 'email' , 'comment']
         
        widgets = {
            #"phone" : TextInput (attrs = { 'placeholder': 'телефон' , 'class': 'f1'}), уже в сессии из сендкода
            "name": TextInput (attrs = { 'placeholder': 'ИМЯ (рекомендуется)' , 'class': 'f1'}),
            "sername": TextInput (attrs = { 'placeholder': 'ФАМИЛИЯ (рекомендуется)' , 'class': 'f1'}),
            "email": TextInput (attrs = { 'placeholder': 'EMAIL (необходимо)' , 'class': 'f1' , 'type' : "email"}),  
            "adress": TextInput (attrs = { 'placeholder': 'АДРЕСС ДОСТАВКИ (необходимо)' , 'class': 'f1'}),  
            "comment": TextInput (attrs = { 'placeholder': 'КОМЕНТАРИЙ И ПОЖЕЛАНИЯ' , 'class': 'f1'}),                             
            }

class CodeForm(forms.Form):
    code = forms.CharField(max_length=20 , label="Код из смс:")
