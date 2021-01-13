from django.shortcuts import render

def home_screen_view(request, *args, **kwargs):
	template_name = "personal/home.html"
	context = {}
	return render(request, template_name, context)