from django.contrib import admin
from zstuoj.practice.models import *

class UsersAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'nick', 'solved', 'accesstime', 'defunct')
	search_fields = ('user_id', 'nick')
	ordering = ('solved', )

class ProblemAdmin(admin.ModelAdmin):
	list_display = ('problem_id', 'title', 'accepted', 'source', 'defunct')
	search_fields = ('problem_id', 'title')
	ordering = ('-problem_id', )
	exclude = ('problem_id', )

class ContestAdmin(admin.ModelAdmin):
	list_display = ('contest_id', 'title', 'start_time', 'end_time', 'private', 'defunct')
	search_fields = ('contest_id', 'title')
	ordering = ('-contest_id', )

class LoginlogAdmin(admin.ModelAdmin):
	list_display = ('log_id', 'user_id', 'password', 'time', 'ip')
	search_fields = ('user_id', )
	ordering = ('-log_id', )

class ExamAdmin(admin.ModelAdmin):
	list_display = ('exam_id', "title", "start_time", "end_time", "private", "defunct")
	search_fields = ("title", )
	ordering = ('-exam_id', )

class ExamProblemAdmin(admin.ModelAdmin):
	ordering = ('-exam_id', 'num')
	exclude = ('exam_id', )

class TfProblemAdmin(admin.ModelAdmin):
	list_display = ('problem_id', 'author_id', 'chapter_id',
			'description', 'answer', 'submit', 'solved', 'defunct')
	search_fields = ("title", "author_id")
	ordering = ('-problem_id', )
	exclude = ('problem_id', )

class SelectProblemAdmin(admin.ModelAdmin):
	list_display = ('problem_id', 'author_id', 'chapter_id',
			'description', 'answer', 'submit', 'solved', 'defunct')
	search_fields = ("title", "author_id")
	ordering = ('-problem_id', )
	exclude = ('problem_id', )

class PrivilegeAdmin(admin.ModelAdmin):
	list_display = ("user_id", "rightstr")
	search_fields = ("user_id", "rightstr")
	exclude = ("privilege_id", )

admin.site.register(Users, UsersAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Loginlog, LoginlogAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamProblem, ExamProblemAdmin)
admin.site.register(TfProblem, TfProblemAdmin)
admin.site.register(SelectProblem, SelectProblemAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
