# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	  * Rearrange models' order
#	  * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from datetime import datetime

class Users(models.Model):
	user_id = models.CharField(max_length=20, primary_key=True)
	email = models.CharField(max_length=100, blank=True)
	submit = models.IntegerField(null=True, blank=True)
	solved = models.IntegerField(null=True, blank=True)
	defunct = models.CharField(max_length=1)
	ip = models.CharField(max_length=20)
	accesstime = models.DateTimeField(null=True, blank=True)
	volume = models.IntegerField()
	language = models.IntegerField()
	password = models.CharField(max_length=32)
	reg_time = models.DateTimeField(null=True, blank=True)
	nick = models.CharField(max_length=100)
	school = models.CharField(max_length=100)
	class Meta:
		db_table = u'users'
	def __unicode__(self):
		return self.user_id

class ProblemManager(models.Manager):
	def problem_list(self, page=1, keyword='', uid=''):
		start_pid = (page-1)*100+1000
		end_pid = start_pid+100
		if keyword:
			plist = self.filter(title__icontains=keyword)
		else:
			plist = self.filter(problem_id__gte=start_pid).filter(problem_id__lt=end_pid)
		plist = plist.values('problem_id', 'title', 'accepted', 'submit')

		if uid:
			has_ac = Solution.objects.user_aclist(uid, start_pid, end_pid)
			for idx in xrange(len(plist)):
				pid = plist[idx]['problem_id']
				if has_ac.has_key(pid):
					plist[idx]['has_ac'] = has_ac[pid]
				else:
					plist[idx]['has_ac'] = 0
		return plist

class Problem(models.Model):
	problem_id = models.IntegerField(null=True, blank=True, primary_key=True)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	input = models.TextField(blank=True)
	output = models.TextField(blank=True)
	input_path = models.CharField(max_length=255, blank=True)
	output_path = models.CharField(max_length=255, blank=True)
	sample_input = models.TextField(blank=True)
	sample_output = models.TextField(blank=True)
	hint = models.TextField(blank=True)
	source = models.CharField(max_length=100, blank=True)
	sample_program = models.CharField(max_length=255, db_column='sample_Program', blank=True) # Field name made lowercase.
	in_date = models.DateTimeField(null=True, blank=True)
	time_limit = models.IntegerField(default=1)
	memory_limit = models.IntegerField(default=64)
	defunct = models.CharField(max_length=1, default='N')
	contest_id = models.IntegerField(null=True, blank=True)
	accepted = models.IntegerField(null=True, blank=True, default=0)
	submit = models.IntegerField(null=True, blank=True, default=0)
	ratio = models.IntegerField(default=0)
	error = models.IntegerField(null=True, blank=True, default=0)
	difficulty = models.IntegerField(default=0)
	submit_user = models.IntegerField(null=True, blank=True, default=0)
	solved = models.IntegerField(null=True, blank=True, default=0)
	case_time_limit = models.IntegerField(default=1)
	spj = models.IntegerField(default=0)

	objects = ProblemManager()
	class Meta:
		db_table = u'problem'

	def __unicode__(self):
		return self.title


class ContestManager(models.Manager):
	def active_contest(self):
		contest_list = self.filter(end_time__gt=datetime.now()).\
				filter(defunct='N').values("contest_id")
		cid_list = [c['contest_id'] for c in contest_list]
		return cid_list


class Contest(models.Model):
	contest_id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=255, blank=True)
	start_time = models.DateTimeField(null=True, blank=True)
	end_time = models.DateTimeField(null=True, blank=True)
	defunct = models.CharField(max_length=1)
	description = models.TextField(blank=True)
	private = models.IntegerField()
	langmask = models.IntegerField()

	objects = ContestManager()
	class Meta:
		db_table = u'contest'

	def __unicode__(self):
		return self.title

class Compileinfo(models.Model):
	solution_id = models.IntegerField(primary_key=True)
	error = models.TextField(blank=True)
	class Meta:
		db_table = u'compileinfo'

class ContestProblem(models.Model):
	problem_id = models.IntegerField()
	contest_id = models.IntegerField(null=True, blank=True)
	title = models.CharField(max_length=200)
	num = models.IntegerField()
	class Meta:
		db_table = u'contest_problem'

class Loginlog(models.Model):
	log_id = models.IntegerField(primary_key=True)
	user_id = models.CharField(max_length=20)
	password = models.TextField(blank=True)
	ip = models.CharField(max_length=100, blank=True)
	time = models.DateTimeField(null=True, blank=True)
	class Meta:
		db_table = u'loginlog'
	def __unicode__(self):
		return u"login log %d"%self.log_id

class Mail(models.Model):
	mail_id = models.IntegerField(primary_key=True)
	to_user = models.CharField(max_length=20)
	from_user = models.CharField(max_length=20)
	title = models.CharField(max_length=200)
	content = models.TextField(blank=True)
	new_mail = models.IntegerField()
	reply = models.IntegerField(null=True, blank=True)
	in_date = models.DateTimeField(null=True, blank=True)
	defunct = models.CharField(max_length=3)
	class Meta:
		db_table = u'mail'

class Message(models.Model):
	message_id = models.IntegerField(primary_key=True)
	problem_id = models.IntegerField()
	parent_id = models.IntegerField()
	thread_id = models.IntegerField()
	depth = models.IntegerField()
	ordernum = models.IntegerField(db_column='orderNum') # Field name made lowercase.
	user_id = models.CharField(max_length=20)
	title = models.CharField(max_length=200)
	content = models.TextField(blank=True)
	in_date = models.DateTimeField(null=True, blank=True)
	defunct = models.CharField(max_length=1)
	class Meta:
		db_table = u'message'

class News(models.Model):
	news_id = models.IntegerField(primary_key=True)
	user_id = models.CharField(max_length=20)
	title = models.CharField(max_length=200)
	content = models.TextField()
	time = models.DateTimeField()
	importance = models.IntegerField()
	defunct = models.CharField(max_length=1)
	class Meta:
		db_table = u'news'

class SolutionManager(models.Manager):
	def user_aclist(self, uid, start_pid=0, end_pid=0):
		if not uid:
			return {}
		ac_list = self.filter(user_id=uid)
		if start_pid > 0:
			ac_list = ac_list.filter(problem_id__gte=start_pid).filter(problem_id__lt=end_pid)
		ac_list = ac_list.values('problem_id')
		wa_list = ac_list.distinct()
		has_ac = {}
		# initialized with 2 for not accept
		for pid in wa_list:
			has_ac[pid['problem_id']] = 2
		ac_list = ac_list.filter(result=4).distinct()
		for pid in ac_list:
			has_ac[pid['problem_id']] = 1
		return has_ac

class Solution(models.Model):
	solution_id = models.IntegerField(primary_key=True)
	problem_id = models.IntegerField()
	user_id = models.CharField(max_length=20)
	time = models.IntegerField()
	memory = models.IntegerField()
	in_date = models.DateTimeField()
	classname = models.CharField(max_length=20, db_column='className') # Field name made lowercase.
	result = models.IntegerField()
	language = models.IntegerField()
	ip = models.CharField(max_length=20)
	contest_id = models.IntegerField(null=True, blank=True)
	valid = models.IntegerField()
	num = models.IntegerField()
	code_length = models.IntegerField()
	judgetime = models.DateTimeField(null=True, blank=True)
	objects = SolutionManager()
	class Meta:
		db_table = u'solution'

	def __unicode__(self):
		return u"[%d]Problem %d of User %s" %(self.solution_id, self.problem_id, self.user_id)

class SourceCode(models.Model):
	solution_id = models.IntegerField(primary_key=True)
	source = models.TextField(blank=True)
	class Meta:
		db_table = u'source_code'


