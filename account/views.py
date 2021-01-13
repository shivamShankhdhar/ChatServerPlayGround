from django.shortcuts import render, redirect
# messages 
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from account.forms import RegistrationForm



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
			destination = kwargs.get("next") # grabbing the requested page when user was not authenticated
			if destination:
				return redirect(destination)
				# messages.info(request, f'Logged In as {email}.')

			return redirect("home")
			# messages.info(request, f'Logged In as {email}.')
		else:
			context['registration_form'] = form

	return render(request, template_name, context)