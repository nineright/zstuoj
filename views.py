from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render

def test(request):
	pages = 31
	page_line_size = 16
	pagelines = [xrange(page, min(page+page_line_size, pages))
		for page in xrange(1,pages, page_line_size)]
	return render(request, 'test.html', {'pagelines': pagelines})


