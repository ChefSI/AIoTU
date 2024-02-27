from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'email']
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name','last_name',  'date_joined', 'api_key', 'api_secret']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'api_key', 'api_secret')}),
    )
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'first_name', 'last_name', 'api_key', 'api_secret', 'password', 'is_staff', 'is_active', 'is_superuser')
                
            ),
        }),
    )
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
    }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
admin.site.register(User, CustomUserAdmin)