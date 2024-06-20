from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name = "home" ),
    path ('ctg/<int:pk>/<int:pk_2>/' , views.cat_page , name = 'category'),
    path ('ctg/<int:pk>/' , views.cat_page , name = 'category'),
    path ('basket_page' , views.basket_page , name = 'basket_page'),
    path ('my_cab' , views.my_cab , name = 'my_cab'),
    path ('sucsess' , views.sucsess , name = 'sucsess'),
    path('signup' , views.signup.as_view() , name = 'signup'),
    path('Login' , views.Login , name = "Login"),
    path('endreg' , views.endreg , name = "endreg"),
    path('edit' , views.edit.as_view() , name = "edit"),
    path('password' , views.password_reset.as_view() , name = "password"),
    path('password2' , views.password_reset2.as_view() , name = "password2"),
    path('usersreset/<uidb64>/<token>/' , views.password_reset3.as_view() , name = "password3"),
    path('product_dv/<id>' , views.product_dv , name = 'product_dv'),
    ]

