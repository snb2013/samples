from django.contrib import admin
from chatbot.models import QuestionList, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    max_num = 5


class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline, )


admin.site.register(QuestionList, admin.ModelAdmin)
admin.site.register(Question, QuestionAdmin)
