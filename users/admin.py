from django.contrib import admin
from users.models import UserProfile, College, Company

class UserProfileAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('name', 'email', 'domain', 'group_name')
    search_fields = ('name', 'user__email')
    
    def email(self, instance):
        return instance.user.email
    
class CollegeAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('name',)
    search_fields = ('name',)
    verbose_name_plural = 'Colleges'

class CompanyAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('name',)
    search_fields = ('name',)
    verbose_name_plural = 'Companies'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Company, CompanyAdmin)