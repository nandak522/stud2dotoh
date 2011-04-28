from django.contrib import admin
from users.models import UserProfile, College, Company, Achievement

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
    
class AchievementAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('title',)
    search_fields = ('title',)
    verbose_name_plural = 'Achievements'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Achievement, AchievementAdmin)
