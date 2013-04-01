import re
from base64 import b64encode, b64decode
from hashlib import md5, sha1
from random import randint


def pw_gen(password, md5ed=False):
	if not md5ed:
		password = md5(password).hexdigest()
	salt = sha1(str(randint(0, 2**31))).hexdigest()[:4]
	hash = b64encode(sha1(password+salt).hexdigest()+salt)
	return hash

def is_old_pw(password):
	return re.match('^[0-9a-fA-F]*$', password)

def pw_check(password, saved):
	if is_old_pw(saved):
		return md5(password).hexdigest() == saved
	salt = b64decode(saved)[-4:]
	hash = b64encode(sha1(md5(password).hexdigest()+salt).hexdigest()+salt)
	return hash == saved

def nl2br(html_str, is_html=True):
	if is_html:
		return html_str.replace('\n', '<br/>\n')
	else:
		return html_str.replace('\n', '<br>\n')


