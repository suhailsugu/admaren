from django.contrib import admin
from apps.users.models import Users
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['id', 'email','username']
    list_display_links = ['email']
    
    
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()
    
    

admin.site.register(Users,UsersAdmin)
