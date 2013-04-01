from django.conf.urls.defaults import patterns, include, url
from zstuoj.practice.views import *
from zstuoj.views import test
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^hello/$', hello),
	url(r'^test/$', test),
	url(r'^meta/$', display_meta),
	url(r'^JudgeOnline/$', homepage),
	url(r'^JudgeOnline/problemset/$', problemset),
	url(r'^JudgeOnline/login/$', login),
	url(r'^JudgeOnline/logout/$', logout),
	url(r'^JudgeOnline/register/$', register),
	url(r'^JudgeOnline/status/$', status),
	url(r'^JudgeOnline/problem/(\d{4})/$', problem),
	url(r'^JudgeOnline/ranklist/', ranklist),
	url(r'^JudgeOnline/userinfo/([0-9a-zA-Z_]{3,20})/', userinfo),
	url(r'^JudgeOnline/submit/(\d{4})/$', submit),
	url(r'^JudgeOnline/showsource/(\d{4,10})/$', showsource),
	url(r'^bootstrap/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': '/home/nineright/codes/djcode/zstuoj/static/bootstrap/'}),
	url(r'^css/(?P<path>.*)', 'django.views.static.serve',
		{'document_root': '/home/nineright/codes/djcode/zstuoj/static/css/'}),
	url(r'^image/(?P<path>.*)', 'django.views.static.serve',
		{'document_root': '/home/nineright/codes/djcode/zstuoj/static/image/'}),
	# Examples:
	# url(r'^$', 'zstuoj.views.home', name='home'),
	# url(r'^zstuoj/', include('zstuoj.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),

)
