from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , product , category , block , order , email_host
from .forms import CustomUserCreationForm, CustomUserChangeForm 

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (*UserAdmin.fieldsets,('доп. инфо:',{'fields':('phone' , 'adress' , 'is_send','was_basket', 'code')}))


class MembershipInline(admin.TabularInline):
    model = product.CAT.through
    extra = 0

class categoryAdmin(admin.ModelAdmin):  
    model = category   
    inlines = [
        MembershipInline,
    ]
    
class productAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ('CAT',)


class blockInline(admin.TabularInline):
    model = block.pro.through
    extra = 3
class blockAdmin(admin.ModelAdmin):    
    inlines = [
        blockInline,
    ]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(product , productAdmin)
admin.site.register(category , categoryAdmin)
admin.site.register(block , blockAdmin)
admin.site.register(order)
admin.site.register(email_host)
# Register your models here.