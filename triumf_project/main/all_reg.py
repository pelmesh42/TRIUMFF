from django.contrib.auth.views import PasswordResetView , PasswordResetDoneView , PasswordResetConfirmView , PasswordResetCompleteView
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.urls import reverse_lazy
import random

from django.shortcuts import render , redirect
from django.views.generic import CreateView , UpdateView , TemplateView , FormView
from .forms import *
from django.http import HttpResponse , JsonResponse
from .models import CustomUser , product
from django.conf import settings
from django.core.mail import send_mail

def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

class signup(FormView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = 'main/users/signup.html'

    def form_valid(self , form):
        print(CustomUser.objects.filter(is_active=False)) 
        form.save()
        uska , creat = CustomUser.objects.get_or_create(email=form.cleaned_data["email"])
        uska.code = generate_code() ; uska.save()
        link ="go to the link : " + self.request.build_absolute_uri('/') + "endreg" + '?link=' + str(uska.code) 
        send_mail(
            "email confirmation",
            link,
            settings.DEFAULT_FROM_EMAIL,
            [form.cleaned_data["email"]],
            fail_silently=False ,
                )
        
        return super().form_valid(form)

def endreg(x):
    mes = ""
    Link = x.GET.get('link') ; print(Link)    
    user = CustomUser.objects.get(code=Link)
    user.is_active = True ; user.save() ; user.code = "0"
    mes = "Всё идеет по плануу!"
    return render(x, 'main/users/endreg.html', {'mes': mes})
   
def Login(x):
    mes = "введите логин и пароль"
    if x.method == 'POST':
        form = LoginForm(x.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(x, user)
                    return redirect('home') 
                else:
                    mes = "Выполните подтверждение через почту"
                    return render(x, 'main/users/login.html', {'form': form , 'mes': mes})

            elif (CustomUser.objects.filter(username=cd['username'] , password=cd['password']).exists()):
                mes = "Выполните подтверждение через почту"
                return render(x, 'main/users/login.html', {'form': form , 'mes': mes})
            elif (CustomUser.objects.filter(username=cd['username']).exists()):
                mes = "неверный пароль и\или не выполнено подтверждение через почту"
                return render(x, 'main/users/login.html', {'form': form , 'mes': mes})
            else:
                mes = "пользователь не существует"
                return render(x, 'main/users/login.html', {'form': form , 'mes': mes})
    else:
        form = LoginForm()
    return render(x, 'main/users/login.html', {'form': form , 'mes': mes})

class password_reset(PasswordResetView):
    template_name = "main/users/password.html"
    success_url = reverse_lazy('password2')
    #email_template_name = 'users/password_email.html'

class password_reset2(PasswordResetDoneView):
    template_name = "main/users/password2.html"

class password_reset3(PasswordResetConfirmView):
    template_name = "main/users/password3.html"
    success_url = reverse_lazy('main/home.html')

class edit(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("home")
    template_name = 'main/users/edit.html'

    def get_object(self):
        return self.request.user
