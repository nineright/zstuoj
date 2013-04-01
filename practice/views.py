from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.http import Http404
from django.shortcuts import render
from django.db.models import Max, Min
from zstuoj.practice.models import Problem, Users, Solution, Loginlog, Contest, ContestProblem, SourceCode
from zstuoj.practice.forms import *
from zstuoj.practice.utils import *
from datetime import datetime


def _update_loginlog(uid, pwd, remote_addr=""):
	log = Loginlog(user_id=uid, password=pw_gen(pwd),
			ip=remote_addr, time=datetime.now())
	log.save()

def _insert_user(cd, remote_addr):
	user = Users(user_id=cd['user_id'], email=cd.get('email'), defunct='N',
			ip=remote_addr, accesstime=datetime.now(), volume=1, language=1,
			password=cd['password'], reg_time=datetime.now(),
			nick=cd['nick'], school=cd['school'])
	user.save()

def _problem_available(pid):
	p = Problem.objects.filter(problem_id=pid).filter(defunct='N').\
			values("problem_id", "defunct")
	if not p.exists() or p[0]['defunct'] == 'Y':
		return False
	pid = p[0]['problem_id']
	cid_list = Contest.objects.active_contest()
	for cid in cid_list:
		if ContestProblem.objects.filter(contest_id=cid).filter(defunct='N').\
				filter(problem_id=pid).exists():
			return False
	return True


def hello(request):
	return HttpResponse("Hello World")

def _get_active_url(req_url):
	active_url = req_url[req_url.find('JudgeOnline')+len('JudgeOnline'):]
	active_url = active_url.strip('/')
	active_url = active_url[:active_url.find('/')]

def _is_admin(request):
	return ("administrator" in request.session) \
		or ('contest_creator' in request.session)

def _get_user_id(request):
	if "user_id" in request.session:
		return request.session['user_id']
	return ""

def oj_header(request):
	nav_urls = [{"name":"Home", "url":"/JudgeOnline/"},
			{"name":"BBS", "url":"/JudgeOnline/bbs"},
			{"name":"Problem Set", "url":"/JudgeOnline/problemset"},
			{"name":"Status", "url":"/JudgeOnline/status"},
			{"name":"Ranklist", "url":"/JudgeOnline/ranklist"},
			{"name":"Contest", "url":"/JudgeOnline/contest"},
			{"name":"Exam", "url":"/JudgeOnline/exam"},
			{"name":"FAQ", "url":"/JudgeOnline/faq"}]
	active_url = _get_active_url(request.path)
	is_admin = _is_admin(request)
	user_id = _get_user_id(request)
	mail = 0
	return {'active_url': active_url,'user_id': user_id,
			'is_admin': is_admin, 'mail': mail,	'nav_urls': nav_urls}

def problemset(request, page='1'):
	keyword = ""
	if request.method == 'GET':
		if 'search' in request.GET:
			keyword = request.GET['search']
		if 'page' in request.GET and request.GET['page']:
			page = request.GET['page']
	try:
		page = int(page)
	except ValueError:
		raise Http404()
	user_id = _get_user_id(request)

	problemlist = Problem.objects.problem_list(page, keyword, user_id)
	max_pid = Problem.objects.aggregate(Max('problem_id')).values()[0]
	if not max_pid:
		max_pid = 0
	pages = (max_pid-1000)/100+1
	pagelines = [xrange(p, min(p+16, pages+1)) for p in xrange(1, pages+1, 16)]
	params = {'problemlist':problemlist, 'pagelines':pagelines, 'cur_page':page}
	params.update(oj_header(request))
	return render(request, 'problemset.html', params)

def login(request):
	# return display_meta(request)
	params = oj_header(request)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				m = Users.objects.get(user_id=cd['username'])
				_update_loginlog(cd['username'], cd['password'],
						request.META.get('REMOTE_ADDR'))
				if m and pw_check(cd['password'], m.password):
					request.session['user_id'] = cd['username']
					referrer = cd['referrer']
					request.session['user_id'] = cd['username']
					return HttpResponseRedirect(referrer)
			except Users.DoesNotExist:
				pass
		params.update({'form':form, 'login_error':True})
		return render(request, 'login.html', params)
	else:
		referrer = request.META.get('HTTP_REFERER')
		if not referrer:
			referrer = "/JudgeOnline/"
		form = LoginForm(initial={'referrer':referrer})
		params.update({'form':form})
		return render(request, 'login.html', params)


def logout(request):
	try:
		del request.session['user_id']
	except KeyError:
		pass
	return HttpResponseRedirect("/JudgeOnline/")

def register(request):
	params = oj_header(request)
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			_insert_user(cd, request.META.get('REMOTE_ADDR'))
			request.session['user_id'] = cd['user_id']
			return HttpResponseRedirect("/JudgeOnline/")
		else:
			params.update({'form':form})
			return render(request, 'register.html', params)
	else:
		form = RegisterForm()
		params.update({'form':form})
		return render(request, 'register.html', params)

def status(request):
	params = oj_header(request)

	lang_list = get_langlist()
	result_list = get_resultlist()
	params.update({"lang_list":lang_list, "result_list":result_list})

	next_top = 0
	pre_top = 0
	top = 0
	filter_list = Solution.objects.all()
	status_list = []
	form = StatusSearchForm(request.GET)
	if form.is_valid():
		cd = form.cleaned_data
		if cd['pid']:
			filter_list = filter_list.filter(problem_id=cd['pid'])
		if cd['uid']:
			filter_list = filter_list.filter(user_id=cd['uid'])
		if cd['lang'] != -1:
			filter_list = filter_list.filter(language=cd['lang'])
		if cd['result'] != -1:
			filter_list = filter_list.filter(result=cd['result'])
		if cd['top']:
			top = cd['top']
			status_list = filter_list.filter(solution_id__lte=cd['top'])\
					.order_by('-solution_id')[:20]
		else:
			top = Solution.objects.aggregate(Max("solution_id")).values()[0]
			# no record in database
			if not top:
				top = 0
			pre_top = top
			if top:
				status_list = filter_list.filter(solution_id__lte=top)\
						.order_by('-solution_id')[:20]
	else:
		params.update({"error":True})
		return render(request, "status.html", params)

	# raise
	status_list = status_list.values("solution_id", "problem_id",
			"user_id", "time", "memory", "in_date", "result",
			"language", "code_length")
	#QuerySet is a iterator and can't modify it directly
	status_list = [r for r in status_list]
	if status_list:
		for i in xrange(len(status_list)):
			status_list[i]["result"] = result_list[status_list[i]["result"]+1]['name']
			status_list[i]["language"] = lang_list[status_list[i]["language"]+1]['name']

		next_top = status_list[-1]['solution_id']-1
		if pre_top == 0:
			pre_page = filter_list.filter(solution_id__gt=top)\
					.order_by('solution_id').values("solution_id")[:20]
			if pre_page.count():
				pre_top = pre_page[pre_page.count()-1]['solution_id']
			else:
				pre_top = top
			# raise
	params.update({"pre_top":pre_top, "next_top":next_top,
		"top":top, "cd":cd,	"status_list":status_list, "error":False})

	# raise
	return render(request, "status.html", params)

def problem(request, pid):
	try:
		pid = int(pid)
	except ValueError:
		raise Http404()
	if not _problem_available(pid):
		raise Http404()
	p = Problem.objects.get(problem_id=pid)
	params = oj_header(request)
	params.update({"p":p})
	return render(request, "problem.html", params)


def ranklist(request):
	start = 0
	if 'start' in request.GET:
		try:
			start = int(request.GET['start'])
		except ValueError:
			pass
	if start < 0:
		start = 0
	user_list = Users.objects.order_by('-solved', 'submit').\
			filter(defunct="N")[start:start+50]
	user_list = user_list.values("user_id", "nick", "solved", "submit")
	params = oj_header(request)
	params.update({"user_list":user_list, "start":start})
	return render(request, "ranklist.html", params)



def submit(request, pid):
	uid = _get_user_id(request)
	if not uid:
		return HttpResponseRedirect("/JudgeOnline/login/")

	params = oj_header(request)
	try:
		pid = int(pid)
	except ValueError:
		raise Http404()
	params["pid"] = pid
	params["lang_list"] = get_langlist(False)
	params["lastlang"] = 1
	if request.method == 'POST':
		form = SubmitForm(request.POST)
		params.update({"form":form})
		if form.is_valid():
			cd = form.cleaned_data
			if not _problem_available(cd['pid']):
				raise Http404()
			next_sid = Solution.objects.aggregate(Max('solution_id')).values()[0]+1
			r = Solution(solution_id=next_sid, problem_id=pid, user_id=uid,
					time=0, memory=0, in_date=datetime.now(), classname="test",
					result=0, language=cd['lang'],
					ip=request.META.get('REMOTE_ADDR'),	valid=1, num=-1,
					code_length=len(cd['source']))
			r.save()
			r = SourceCode(solution_id=next_sid, source=cd['source'])
			r.save()
			return HttpResponseRedirect("/JudgeOnline/status/")
		else:
			return render(request, "submit.html", params)

	return render(request, "submit.html", params)


def userinfo(request, uid):
	user = Users.objects.filter(user_id=uid).filter(defunct='N').\
			values("user_id", "nick", "solved", "submit", "email", "school")
	if not user.exists():
		raise Http404()
	user = user.get()

	attempt_list = Solution.objects.filter(user_id=uid)
	solved_list = attempt_list.filter(result=4).values("problem_id").\
			order_by("problem_id").distinct()
	solved_list = [p["problem_id"] for p in solved_list]
	user['rank'] = Users.objects.filter(solved__gt=user['solved']).count()+1
	params = oj_header(request)
	params.update({"user":user, "solved_list":solved_list})
	# raise
	return render(request, "userinfo.html", params)

def showsource(request, sid):
	uid = _get_user_id(request)
	if not uid:
		return HttpResponseRedirect("/JudgeOnline/login/")
	try:
		sid = int(sid)
	except ValueError:
		raise Http404()

	params = oj_header(request)
	r = Solution.objects.filter(solution_id=sid).values("solution_id",
			"time",	"problem_id", "user_id", "result", "memory",
			"language", "code_length")
	if not r:
		raise Http404()
	r = r[0]
	r['language'] = get_langlist()[r['language']+1]['name']
	r['result'] = get_resultlist()[r['result']+1]['name']
	if r['user_id'] == uid or _is_admin():
		src = SourceCode.objects.filter(solution_id=sid).values("source")
		if not src.exists():
			raise Http404()
		source = src[0]['source']
		params['source'] = source
		params['solution'] = r
		return render(request, "showsource.html", params)

	else:
		raise Http404()


def homepage(request):
	params = oj_header(request)
	return render(request, 'index.html', params)


def display_meta(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' %(k, v))
	return HttpResponse('<table>%s</table>' % '\n'.join(html))

