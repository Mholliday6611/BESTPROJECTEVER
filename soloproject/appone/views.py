from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from models import *
from forms import UserForm, UserProfileForm, PostForm, CategoryForm, PageForm, ContactForm, PasswordRecoveryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin
# Create your views here.

def index(request):
	context_dict = {}
	popular_post = Post.objects.order_by('-likes' )[:5]
	
	context_dict['post'] = popular_post


	response = render(request, 'index.html', context_dict)
	return response

def about(request):
	context_dict = {}

	return render(request, 'about.html', context_dict)

def Posts(request, post_name_slug):
	context_dict = {}
	try:
		post = Post.objects.get(slug=post_name_slug)
		
		context_dict['post'] = post

	except Post.DoesNotExist:
		pass

	return render(request, 'post.html', context_dict)

@login_required
def AddPost(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			print "test"
			p = form.save(commit=False)
			p.user = request.user
			p.save()
			return index(request)
		else:
			print form.errors
	else:
		form = PostForm()

	context_dict = {'form':form}

	return render(request, 'add-post.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None

	if request.method == 'POST':
		query= request.POST['query'].strip()

		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list
			context_dict['query'] = query

	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category).order_by('-views')

		context_dict['category'] = category
		context_dict['pages'] = pages

	except Category.DoesNotExist:
		pass

	return render(request, 'category.html', context_dict)

@login_required
def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat= None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page= form.save(commit=False)
				page.user = request.user
				page.category = cat
				page.views = 0 
				page.save()
				return category(request, category_name_slug)
			else:
				print form.errors
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form':form, 'category': cat, 'slug': category_name_slug}

	return render(request, 'add-page.html', context_dict)

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)

			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'register.html', {'user_form' : user_form,
											 'profile_form': profile_form,
											 'registered':registered}
											 )

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username ,password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse('Your account is inactive')
		else:
			print "Invalid login details : {0}, {1}".format(username, password)
			return HttpResponse('Your login credentials were wrong')
	else:
		return render(request, 'login.html', {})
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def user_profile(request, user_username):
	context_dict = {}
	user = User.objects.get(username=user_username)
	profile = UserProfile.objects.get(user=user)
	context_dict['profile'] = profile
	context_dict['pages'] = Page.objects.filter(user=user)
	context_dict['posts'] = Post.objects.filter(user=profile)


	return render(request, 'profile.html', context_dict)

@login_required
def edit_profile(request, user_username):
	profile = get_object_or_404(UserProfile, user__username=user_username)
	website = profile.website
	pic = profile.picture
	bio = profile.bio
	if request.user != profile.user:
		return HttpResponse('Access Denied Loser')

	if request.method == 'POST':
		form = UserProfileForm(data=request.POST)
		if form.is_valid():
			if request.POST['website'] and request.POST['website'] != '':
				profile.website = request.POST['website']
			else:
				profile.website = website

			if request.POST['bio'] and request.POST['bio'] != '':
				profile.bio = request.POST['bio']
			else:
				profile.bio = bio

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			else:
				profile.picture = pic

			profile.save()

			return user_profile(request, profile.user.username)

		else:
			print form.errors
	else:
		form = UserProfileForm()
	return render(request, 'edit_profile.html', {'form':form, 'profile':profile}) 

@login_required
def like_category(request):
	cat_id= None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()
	return HttpResponse(likes)


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)

		if form.is_valid():
			form.send_message()

			return HttpResponseRedirect('/')
		else:
			print form.errors
	else:
		form = ContactForm()
	return render(request, 'contact.html', {'form':form})

class SettingsView(LoginRequiredMixin, FormView):
	template_name = 'settings.html'
	form_class = PasswordChangeForm
	success_url = reverse_lazy('index')

	def get_form(self, form_class):
		return form_class(user=self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self, request, form.user)
		return super(SettubgView, self).form_valid(form)

class PasswordRecoveryView(FormView):
	template_name = "password-recovery.html"
	form_class = PasswordRecoveryForm
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		form.reset_email()
		return super(PasswordRecoveryView, self).form_valid(form)

def track_url(request):
	post_id = None 
	url = '/'
	if request.method == 'GET':
		if 'post_id' in request.GET:
			post_id = request.GET['post_id']
			try:
				post = Post.objects.get(id=post_id)
				post.views = post.views + 1
				post.save()
				url = post.url
			except:
				pass
	return redirect(url)

