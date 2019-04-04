
#django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#models
from django.contrib.auth.models import User
from users.models import Profile

# Register your models here.
#admin.site.register(Profile) #forma sencilla de registrar un modelo en la pagina de admin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin"""
    list_display = ('pk', 'user', 'phone_number', 'website', 'picture') #este para editar la forma en la que sse proesenta cada registro
    list_display_links = ('pk','user') #para condigurar que campos van ahacer links 
    list_editable = ('phone_number', 'website', 'picture') #para condifurara que campos son editables
    search_fields = ('user__email', 'user__username','user__first_name', 'user__last_name', 'phone_number') #campos por las cuales se realizaran las busquedas
    list_filter = ('user__is_active', 'user__is_staff', 'created', 'modified') #agregar los filtros

    #para configurara la interfaz de los detalles de profile. Se realiza por medio de tuplas 

    fieldsets = (
        ('Profile', {
            'fields': (('user', 'picture'),),
        }),
        ('Extra Info', {
            'fields': (
                ('website', 'phone_number'),
                ('biography')
            )
        }),
        ('Metadata', {
            'fields': (('created', 'modified'),),
        }),
    )

    readonly_fields = ('created', 'modified',)


#Asignar un el profile en amdin de users

class ProfileInline(admin.StackedInline):
    """Profile in-line admin for users"""

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

    
class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin"""

    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

