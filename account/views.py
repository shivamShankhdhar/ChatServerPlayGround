from django.shortcuts import render, redirect
# messages 
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AccountAuthenticationForm



def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return HttpResponse(f"You are already authenticated as {user.email}.")

	context = {}
	template_name = 'account/register.html'
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email = email, password= raw_password)
			login(request, account)
			messages.success(request, f"Logged In as ' {email} '.")
			destination = get_redirect_if_exists(request) # grabbing the requested page when user was not authenticated
			if destination:
				return redirect(destination)
				# messages.info(request, f'Logged In as {email}.')

			return redirect("home")
			# messages.info(request, f'Logged In as {email}.')
		else:
			context['registration_form'] = form

	return render(request, template_name, context)



def login_view(request, *args, **kwargs):
	template_name = 'account/login.html'
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("home")
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email 		= request.POST['email']
			password 	= request.POST['password']
			user = authenticate(email = email, password = password)
			if user:
				login(request, user)
				messages.success(request, f"User logged in as ' {email}' ")
				destination = get_redirect_if_exists(request)
				if destination:
					return redirect(destination)
				return redirect("home")
		else:
			context['login_form'] = form

	return render(request, template_name, context)

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def logout_view(request):
	logout(request)
	messages.success(request, "User Logged out Successfully .")
	return redirect("home")

