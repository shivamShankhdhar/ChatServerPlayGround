from django.shortcuts import render, redirect
# messages 
from django.contrib import messages
from account.models import Account
# settings 
from django.conf import settings

from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm



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


def account_view(request, *args, **kwargs):
	# Logic-
	# 	is_self :
	# 		is_friend:
	# 			-1: NO_REQUEST_SENT
	# 			 0: THEM SENT_TO_YOU
	# 			 1:YOU_SENT_THEM

	template_name 	= 'account/account.html'
	context		  	= {}
	user_id 		= kwargs.get("user_id")
	try:
		account 	= Account.objects.get(pk = user_id)
	except Account.DoesNotExist:
		return HttpResponse("<center><h1>Account doesn't exist.</h1></center>")
	if account:
		context['id'] 			 = account.id
		context['username'] 	 = account.username
		context['email'] 		 = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] 	 = account.hide_email

		# state template variables
		is_self = True
		is_friend = False
		user = request.user

		# check for user authenticated and not looking for own profile
		if user.is_authenticated and user != account:
			is_self = False 	
		elif not user.is_authenticated:
			is_self = False
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL

		return render(request, template_name, context)

def account_search_view(request, *args, **kwargs):
	template_name = 'account/search_result.html'
	context = {}
	if request.method == "GET":
		serach_query = request.GET.get("q")
		# print(serach_query)
		context['serach_query'] = serach_query
		if len(serach_query) > 0:
			search_results = Account.objects.filter(email__icontains = serach_query).filter(username__icontains = serach_query).distinct()
			# user = request.user
			accounts = [] #[(account1, True/False),(account2, True/False) ] in this list logic goes as --- index:0- account index:1 friend status
			for account in search_results:
				accounts.append((account, False))
			context['accounts'] = accounts
		# 	context['serach_query'] = serach_query
		# context['serach_query'] = serach_query

	return render(request, template_name, context)


def edit_account_view(request, *args, **kwargs):
	template_name = "account/edit_account.html"

	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk = user_id)
	except Account.DoesNotExist:	
		return HttpResponse("Something went wrong.")
	if account.pk != request.user.pk:
		return HttpResponse("You can't edit someone else profile.")
	context  = {}	
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance = request.user)
		if form.is_valid():
			form.save()
			return redirect("account:view", user_id = account.pk)
		else:
			# when the form is invalid populate the form with the initial values
			form = AccountUpdateForm(request.POST, instance = request.user, 
				initial = {
					'id':account.pk,
					'email':account.email,
					'username':account.username,
					'profile_image':account.profile_image,
					'hide_email':account.hide_email,
					'is_private':account.is_private,
				}
			)
			context['form'] = form
	# when the request is not post request
	else:
		form = AccountUpdateForm(
			initial = {
				'id':account.pk,
				'email':account.email,
				'username':account.username,
				'profile_image':account.profile_image,
				'hide_email':account.hide_email,
				'is_private':account.is_private,
			}
		)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, template_name, context)


