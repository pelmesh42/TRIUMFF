import email
from django.shortcuts import render , redirect
from django.views.generic import CreateView , UpdateView , TemplateView , FormView
from .forms import *
from django.views.generic import DetailView
from django.http import HttpResponse , JsonResponse
from .models import CustomUser , product , block , category , footer , order , email_host
from django.core.paginator import Paginator
from .all_reg import *
from django.template.loader import render_to_string
from smsaero import SmsAero
from pprint import pprint

import datetime
now = datetime.datetime.now()
import random
#глобальные переменные - не трогать
chek = True
alarma = False
#функции:
#функция отправки сообщения
user_to_send =[]
order_form_onsite = order_f()

def send (x , y):
      send_mail (
          'TRIUMFF',
          y,
          settings.DEFAULT_FROM_EMAIL,
          x,
          fail_silently=False ,          
      )
#функция корзины
bsk_data = {} ;
def basket_mech (x):
    global chek
    if x.session.get('bas') is None:
        x.session['bas'] = {}
        print("session reset , try again")
        
    print(x.POST)
    ID = x.POST.get ('to_basket');
    # QW = x.POST.get ('quantity');
    if 'to_basket' in x.POST:          
        for el in product.objects.all() : #Фактически универсальная часть, но  не необходимая
            if int(ID) == int (el.id) :

                # if int(x.POST['quantity']) > int(el.amount):
                #     global alarma; alarma = True
                #     return redirect ('main/home.html')

                if x.session['bas'] != None :
                    bsk_data = x.session['bas']

                if str(el.id) in bsk_data:
                    if int(x.POST['quantity']) == 0:
                        print("mayak1")
                        bsk_data.pop(str(el.id) , None)
                        x.session['bas'] = bsk_data
                        return 0
                    bsk_data[str(el.id)] = x.POST['quantity']
                  
                    x.session['bas'] = bsk_data
                    chek = False

                if chek :                 
                    if int(x.POST['quantity']) == 0:
                        print("mayak2")
                        bsk_data.pop(str(el.id) , None)
                        x.session['bas'] = bsk_data
                        return 0
                    bsk_data[int(el.id)] = x.POST['quantity']
                    
                    x.session['bas'] = bsk_data
                chek = True


#_________________________________________________#
    ID = x.POST.get ('delete_from_basket');
    if 'delete_from_basket' in x.POST:
        for el in product.objects.all() :
            if int(ID) == int (el.id) : 
                if x.session['bas'] != None :
                    bsk_data = x.session['bas']                
                bsk_data.pop(str(el.id) , None)
                x.session['bas'] = bsk_data
#функция лайка
like_data = [];
def like_mech (x):
    if x.session.get('fav') is None:
        x.session['fav'] = []
        print("session reset , try again")

    ID = x.POST.get ('to_like');
    print(x.POST)
    if 'to_like' in x.POST:          
        for el in product.objects.all() :
            if int(ID) == int (el.id) :
                if x.session['fav'] != None :
                    like_data = x.session['fav']
                if not(str(el.id) in str(x.session.get('fav'))):
                    like_data.append(el.id)
                    x.session['fav'] = like_data

    ID = x.POST.get ('delete_from_like');
    if 'delete_from_like' in x.POST:
        for el in product.objects.all() :
            if int(ID) == int (el.id) : 
                if x.session['fav'] != None :
                    like_data = x.session['fav']
                like_data.remove(el.id)
                x.session['fav'] = like_data

def sms_code(x):
        #order_form_onsite = order_f(x.POST)
        now = datetime.datetime.now()
        x.session['pho'] = x.GET.get('phone', None)
        print(x.session['pho'] , "<-----" , x.GET.get('phone', None))
        random.seed(now.microsecond)
        four = []; four.append (int(random.randrange(0 , 9)));four.append (int(random.randrange(0 , 9)));four.append (int(random.randrange(0 , 9)));four.append (int(random.randrange(0 , 9)));
        x.session['cod'] = []
        x.session['cod'] = four

            #api = SmsAero('arabicatest7@gmail.com', 'WXEEtMZ2ZT3XHJhEJJOhyaEcCZ7U') !!!!!!!!!!!
            #print(api.send(str(x.session.get('pho')) , str(x.session.get('cod')))) !!!!!!!!!!!!!
            #сюда высылка кода
        print(x.session['cod'])

def get_basket_fields(x):
        x.session['name'] = x.POST.get('name', None)
        x.session['sername'] = x.POST.get('sername', None)
        x.session['email'] = x.POST.get('email', None)
        x.session['adress'] = x.POST.get('adress', None)
        x.session['comment'] = x.POST.get('comment', None)
                
def formation(x):
    mess_to_send = ""
    full_price = 0;
    new_order = order();
    user_who_send = email_host.objects.all() 
   
    for el_2 in CustomUser.objects.all():                        
        if el_2.is_send:           
            global user_to_send; user_to_send.append(str(el_2.email))

                #___________формирование сообщения заказа____________
    for el in product.objects.all() :     
        if str(el.id) in x.session.get('bas').keys():          
            mess_to_send += str(el.name) + "-по цене:" + str(el.price) + " В количестве "+ str(x.session.get('bas')[str(el.id)]) +" единиц " + "Сумма" + str(el.price*int(x.session.get('bas')[str(el.id)]))+"\n"
            full_price+=int(el.price)*int(x.session.get('bas')[str(el.id)]); print(full_price);

    mess_to_send += "\n" + "Финальная сумма-" + str(full_price) + "\n" +"Телефон:"+str(x.session.get('pho'))+"\n" + "адрес:" + str(x.session.get('adress'))+"\n" + "почта:" + str(x.session.get('email'))+"\n" + "АДРЕС ДОСТАВКИ" + str(x.session.get('adress'))+"\n"  + "пожелание" + str(x.session.get('comment'))
                #___________формирование сообщения заказа____________
    send(user_to_send , mess_to_send) 
    new_order.phone = str(x.session.get('pho'))
    new_order.adress = str(x.session.get('email'))
    new_order.phone = str(x.session.get('name'))
    new_order.phone = str(x.session.get('sername'))
    new_order.adress = str(x.session.get('adress'))
    new_order.desc = mess_to_send
    new_order.save();

    for el in product.objects.all():           
        if str(el.id) in x.session.get('bas').keys():               
            new_order.products.add(el);
        print(new_order.products)

def amount_chek(x):
    zaeb = True
    in_bsk = x.session['bas'].copy()

    for el in in_bsk.keys():
        if (int(product.objects.get(pk = int(el)).amount) - int(in_bsk[el])) < 0:
            zaeb = False

    if zaeb == True:
        for el in in_bsk.keys():
            m = product.objects.get(pk = int(el))
            m.amount = m.amount - int(in_bsk[el])
            m.save()
    return zaeb
      
def from_to (x):
    try:
        user = CustomUser.objects.get(phone = x.session.get('pho'))
        if user is not None:        
            if user.is_active:                           
                login(x, user)
                x.user.was_basket = x.session['bas'] ;
                x.user.save()
                x.session['bas'] = {}
    except:
        user = CustomUser.objects.create_user(username = str(x.session.get('pho')) , phone = x.session.get('pho'))      
        user.is_active = True ;
        try:
            user.was_basket.update(x.session['bas']);
        except:
            user.was_basket = x.session['bas'] ;
        user.username == str(x.session.get('pho'))
        user.save()
        login(x, user)
        x.session['bas'] = {}

    foot = footer.objects.all()
    ctg_on_site = category.objects.all()
    to_blocks_down = block.objects.all()[:3]
  
    
def my_cab(x):   
    #_____________________получение товаров_______________
    bsk_data_now = []     #код несократим по тех.причинам
    for el in product.objects.all():
        if not x.user.is_anonymous:
            for mel in list(x.user.was_basket.keys()):
                if (str(el.id) == mel):
                    bsk_data_now.append(el)
                    
    
    if x.is_ajax():       

        data = {}
        if x.GET.get('result', None) and 'send_code' in x.GET.get('result', None):     
            x.session['pho'] = x.GET.get('phone', None)
            try:                         
                user = CustomUser.objects.get(phone = x.session.get('pho'))      
                if user.is_active:                           
                    login(x, user)     
                    data = {'active':"True"}
            except:
                pass
                data = {'alert':"незарегистрированный номер телефона"}
                # user = CustomUser.objects.create_user(username = str(x.session.get('pho')) , phone = x.session.get('pho') , email="noemailyet@mail.com" , code="3420658133807096")      
                # user.is_active = True ;
                # user.save()
                # login(x, user)
            
            # data = {'code': ''.join([str(x) for x in x.session['cod']])} 
            return JsonResponse(data)    
                          
    foot = footer.objects.all()
    return render (x , 'main/my_cab.html' , {'foot' : foot , 'pib' : bsk_data_now})


def sucsess(x):
    return render(x , 'main/bas_success.html')

def fail(x):
    return render(x , 'main/bas_fail.html')

def home(x):
    foot = footer.objects.all()
    ctg_on_site = category.objects.all()
    to_blocks_down = block.objects.all()[:3]

    return render (x , 'main/home.html' , {'foot' : foot , 'ctg_on_site' : ctg_on_site ,'to_blocks_down' :to_blocks_down})

def product_dv(x, id):
    Tech_name = product.objects.get(id = id).tech_name 
    another_size_products = product.objects.filter(tech_name = Tech_name)
    main_product = product.objects.get(id = id)    
    th = 'тех.название';
    #_-__-__-_-__Перенос фунций добавления__--__--__--_
    if x.is_ajax(): 
        print(x.GET.get('result', None))
        basket_mech(x);
        like_mech(x);
        s_data = x.session.get('fav').copy()
        b_data = list(x.session.get('bas').keys()); b_data = [int(item) for item in b_data]
        b_data_amount = x.session.get('bas'); 
    else:
        basket_mech(x);
        like_mech(x);
        s_data = x.session.get('fav').copy()
        b_data = list(x.session.get('bas').keys()); b_data = [int(item) for item in b_data]
        b_data_amount = x.session.get('bas'); 
    #_-__-__-_-__Перенос фунций добавления__--__--__--_
    return render(x, "main/product_dv.html", {'el': main_product ,'vr': another_size_products ,'th':th ,  's_data' : s_data , 'b_data' : b_data ,})

def cat_page(x , pk , pk_2=1):    
    amount = 9;
    ctg_on_site = category.objects.all()
    basket_mech(x);
    like_mech(x);
    s_data = x.session.get('fav').copy()
    b_data = list(x.session.get('bas').keys()); b_data = [int(item) for item in b_data]
    b_data_amount = x.session.get('bas'); 
    foot = footer.objects.all()

    if x.is_ajax():  

        product_on_site = product.objects.filter(CAT = pk).filter(name__in=list(product.objects.values_list('name', flat=True).distinct()))
        product_on_site = product.objects.filter(CAT = pk)  
        page = Paginator(product_on_site , amount).page(pk_2)

        html = render_to_string('main/products.html' , {
                    'NAME' : category.objects.get(pk=pk).name ,
                    'foot' : foot ,
                    'page_obj': page,
                    'product_on_site' : page.object_list ,
                    's_data' : s_data ,
                    'b_data' : b_data ,
                    'b_data_gramm' : b_data_amount ,
                    'alarma' : alarma,
                    'ctg_on_site' : ctg_on_site,
                    'pk': pk,
                    }) 
        return JsonResponse (html , safe=False)

    else:

        product_on_site = product.objects.filter(CAT = pk).filter(name__in=list(product.objects.values_list('name', flat=True).distinct()))
        page = Paginator(product_on_site , amount).page(pk_2)
        return render (x, 'main/products.html' , 
                    {
                    'NAME' : category.objects.get(pk=pk).name ,
                    'foot' : foot ,
                    'page_obj': page,
                    'product_on_site' : page.object_list ,
                    's_data' : s_data ,
                    'b_data' : b_data ,
                    'b_data_gramm' : b_data_amount ,
                    'alarma' : alarma,
                    'ctg_on_site' : ctg_on_site,
                    'pk': pk,
                    'pk_2':pk_2,
                    })

def basket_page (x):
        #_-__-__-_-__Перенос фунций добавления__--__--__--_
    if x.is_ajax(): 
        basket_mech(x);
        like_mech(x);
        s_data = x.session.get('fav').copy()
        b_data = list(x.session.get('bas').keys()); b_data = [int(item) for item in b_data]
        b_data_amount = x.session.get('bas'); 
    else:
        basket_mech(x);
        like_mech(x);
        s_data = x.session.get('fav').copy()
        b_data = list(x.session.get('bas').keys()); b_data = [int(item) for item in b_data]
        b_data_amount = x.session.get('bas'); 
    #_-__-__-_-__Перенос фунций добавления__--__--__--_

    if x.is_ajax():  
        data = {}
        print(x.POST)
        if x.GET.get('result', None) and 'send_code' in x.GET.get('result', None):
            sms_code(x)
            data = {'code': ''.join([str(x) for x in x.session['cod']])} 
            return JsonResponse(data)

        if  x.POST.get('result', None) and 'send_data' in x.POST.get('result', None): 
            get_basket_fields(x)
            print(x.session['adress'] ,  x.session['email']  ,  x.session['name'])
            return JsonResponse(data)

    if  'kassa_bt' in x.POST:   # позже будет переделано под робокассу что разрешит нюанс              
        if amount_chek(x):
            formation(x)
            from_to(x)
            return redirect('sucsess')
        else:
            return redirect('main/basket.html')
    #buy(x);
    bsk_data_now = {}
    b_data_gramm = {}
    price_data_now = {}
    #_____________________получение товаров_______________
    bsk_data_now = []     #код несократим по тех.причинам
    for el in product.objects.all():
        if x.session.get('bas') != None:
            for mel in list(x.session.get('bas').keys()):
                if (str(el.id) == mel):
                    bsk_data_now.append(el)
    #____________________________________________________

    #___________________подсчет цены___________________
    if x.session.get('bas') != None:
        price_data_now = x.session.get('bas').copy()
        c = 0
        for el in price_data_now.keys():
            price_data_now[el] = int(price_data_now[el])
            price_data_now[el] *= bsk_data_now[c].price
            c+=1
     #________________________________________________
    if x.session.get('bas') != None:
        b_data_gramm = x.session.get('bas');
    foot = footer.objects.all()

    return render (x , 'main/basket.html' ,
                  { 'foot' : foot ,

                    's_data' : s_data ,
                    'b_data' : b_data ,
                    'b_data_gramm' : b_data_amount ,

                    'price': price_data_now,
                    'product_on_site' : bsk_data_now ,
                    'buy_out' : order_form_onsite ,
                    #'code_out' : code_form_onsite ,
                    'b_data_gramm' : b_data_gramm})
# Create your views here.


