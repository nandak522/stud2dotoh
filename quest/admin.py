from django.contrib import admin
from quest.models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('title', 'raised_by', 'closed')
    search_fields = ('title',)
    list_filter = ('closed', 'raised_by')
    
class AnswerAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('question', 'given_by', 'accepted')
    search_fields = ('description',)
    list_filter = ('accepted', 'given_by')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)