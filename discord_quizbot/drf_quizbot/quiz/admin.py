from django.contrib import admin

from .models import Answer, Question


class AnswerInlineModel(admin.TabularInline):
    model = Answer
    fields = ("answer", "is_correct")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ("title", "points", "difficulty", "is_active")
    list_display = ("title", "updated_at", "is_active")
    inlines = (AnswerInlineModel,)


@admin.register(Answer)
class AdminAnser(admin.ModelAdmin):
    list_display = ("answer", "is_correct", "question")
