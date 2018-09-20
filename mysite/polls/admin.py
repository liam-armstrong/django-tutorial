from django.contrib import admin
from .models import *

admin.site.register(Choice)

class ChoiceInLine(admin.Tabular        Inline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']})
        ('Date Information', {'fields': ['pub_date']})]
    inlines = [Choiceinline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
        
admin.site.register(Question, QuestionAdmin)