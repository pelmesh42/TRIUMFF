from wsgiref import validate
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from phonenumber_field.modelfields import PhoneNumberField
from jsonfield import JSONField

def changer(mail , ps):
    settings.EMAIL_HOST_USER = mail;
    settings.EMAIL_HOST_PASSWORD = ps;
    print(settings.EMAIL_HOST_USER)
    print(settings.EMAIL_HOST_PASSWORD)

#class my_color(models.Model):
#    color_code = models.CharField (max_length=200, default ='Название')  
#------------------------------product-------------------------------------#
class category(models.Model):
    name = models.CharField (max_length=200, default ='Название')   
    color = models.CharField (max_length=400, default ='Название')   
    def get_absolute_url(self):
         return f'/ctg/{self.pk}/'     
#-------------------------------------------------------------------------#
class product(models.Model):
    name = models.CharField (max_length=200, default ='Название')   
    desc = models.TextField('Сжатое описание' , blank = True)
    full_desc = models.TextField('Полное описание' , blank = True)
    COMPOSITION = models.TextField('СОСТАВ И УХОД' , blank = True)
    MEASUREMENTS = models.TextField('ОБМЕРЫ' , blank = True)
    #REVIEWS = models.TextField('ОТЗЫВЫ' , blank = True) в дальнейшем перевести на фореигн кей
    image = models.ImageField(upload_to='static\media\img',  blank = True)
    extra_image1 = models.ImageField(upload_to='static\media\img',  blank = True)
    extra_image2 = models.ImageField(upload_to='static\media\img',  blank = True)
    extra_image3 = models.ImageField(upload_to='static\media\img',  blank = True)
    extra_image4 = models.ImageField(upload_to='static\media\img',  blank = True)
    #количество______________________________
    amount = models.IntegerField(default ='0')
    #цена_______________________________________
    price = models.IntegerField(default ='10000')
    discount = models.BooleanField('есть скидка' , default = False)
    old_price = models.IntegerField('старая цена' , default ='999')

    tech_name = models.CharField (max_length=200, default ='тех.название')
    all_size = models.CharField (max_length=200, default ='перечисление размеров')   
    CHOICES = (('XXS', 'XXS'),
               ('XS', 'XS'),
               ('S', 'S'),
               ('M', 'M'),
               ('L', 'L'),
               ('XL', 'XL'),
               ('XXL', 'XXL'),)   
    size = models.CharField (max_length=200 , choices = CHOICES , default = 'M')    

    shown = models.BooleanField('показать' , default = True)
    CAT = models.ManyToManyField(category , null = True , blank = True , related_name='products')
    CAT_on_site = models.ForeignKey(category , null = True , blank = True , on_delete = models.SET_NULL)
    my_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    def __str__ (self):
       return self.name + " " + str(self.size) + "р";
#-------------------------------------------------------------------------#



#---------------------------------User------------------------------------#
class CustomUser(AbstractUser):

    email = models.EmailField(null=False, blank=False, unique=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True, region="RU")
    code = CharField(max_length=16, blank = True)
    adress = models.CharField (max_length=200, default ='Adress' , blank = True)   
    is_active = models.BooleanField(default = False)
    is_send = models.BooleanField(default = False)
    like = models.ManyToManyField(product , null = True , blank = True , related_name='user_that_like')    
    was_basket = JSONField(default = {})
    def __str__(self):
        return self.username + "" + str(self.phone)
#-------------------------------------------------------------------------#   
class rev (models.Model):
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE , null = True , blank = True )
    rev_product = models.ForeignKey(product, on_delete = models.CASCADE , null = True , blank = True )
    prons = models.TextField('Плюсы' , blank = True)
    cons = models.TextField('Минусы' , blank = True)
    body = models.TextField('Комментарий' , blank = True)

#-------------------------------------------------------------------------#
class email_host(models.Model):
    name = models.CharField("имя-константа", max_length=150 , db_index=True , default ='host_of_email')
    email = models.CharField("почта", max_length=150 , db_index=True)
    password = models.CharField("пароль", max_length=150 , db_index=True)
    a_password = models.CharField("пароль sms рассылки", max_length=150 , db_index=True , default ='пароль для рассылки смс')
    a_email = models.CharField("почта sms рассылки", max_length=150 , db_index=True , default ='почта для рассылки смс')
    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)
        changer(self.email , self.password)
#-------------------------------------------------------------------------#


class order(models.Model):
    name = models.CharField (max_length=200, default ='Имя клиента')   
    sername = models.CharField (max_length=200, default ='Фамилия клиента') 
    adress = models.CharField (max_length=200, default ='адрес доставки') 
    phone = models.CharField(null=True, blank=True, max_length=12 , default="+700000000") #unique=True ,
    email = models.EmailField(null=False, blank=False, unique=False, default = "email")
    comment = models.TextField('Коментарий' , blank = True)


    products = models.ManyToManyField(product)
    users = models.ForeignKey(CustomUser, on_delete = models.CASCADE , null = True , blank = True )
    sp_code = CharField(max_length=16, blank = True)
    desc = models.TextField('описание' , blank = True)

    class Meta:
            verbose_name = 'Заказ'
            verbose_name_plural = 'Заказы'

#-------------------------------------------------------------------------#



#---------------------------------block-----------------------------------#
class block(models.Model):
    name = models.CharField (max_length=200, default ='Название блока')   
    img = models.ImageField(upload_to='static\media\img',  blank = True)
    is_img = models.BooleanField(default = False)
    pro = models.ManyToManyField(product , null = True , blank = True , related_name='products')
#-------------------------------------------------------------------------#
class footer(models.Model):
      contact = models.TextField('контакты' , blank = True)
#-------------------------------------------------------------------------#

# Create your models here.
