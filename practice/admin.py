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

class ContestAdmin(admin.ModelAdmin):
	list_display = ('contest_id', 'title', 'start_time', 'end_time', 'private', 'defunct')
	search_fields = ('contest_id', 'title')
	ordering = ('-contest_id', )

class LoginlogAdmin(admin.ModelAdmin):
	list_display = ('log_id', 'user_id', 'password', 'time', 'ip')
	search_fields = ('user_id', )
	ordering = ('-log_id', )

admin.site.register(Users, UsersAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Loginlog, LoginlogAdmin)

