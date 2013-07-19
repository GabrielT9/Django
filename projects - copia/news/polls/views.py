# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from polls.forms import RegistrationForm, LoginForm, NewsForm, CommentForm, NewsDelForm, UpdateNewsForm
from polls.models import News, Person, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max

def show_home(request):
   #users = Person.objects.filter(first_name='Gabriel')
   news = News.objects.all()
   context = {'news': news}
   return render_to_response('home.html', context, context_instance=RequestContext(request))

def show_news(request):
	#user = request.user.pk
	#person = Person.objects.get(user_id=user)
	news = News.objects.all()
	context = {'news': news}
	return render_to_response('listnews.html', context, context_instance=RequestContext(request))

def show_my_news(request):
	user = request.user.pk
	person = Person.objects.get(user_id=user)
	my_news = News.objects.filter(user=person)
	context = {'my_news': my_news}
	return render_to_response('mynews.html', context, context_instance=RequestContext(request))

def show_comments(request, id):
	news = get_object_or_404(News,id=id)
	comments = Comment.objects.filter(news_item=news)
	context = {'comments': comments}
	return render_to_response('listcomments.html', context, context_instance=RequestContext(request))	

def show_my_comments(request, id):
	user = request.user.pk
	person = Person.objects.get(user_id=user)
	news = get_object_or_404(News,id=id)
	comments_per_news = Comment.objects.filter(news_item=news)
	my_comments = comments_per_news.filter(user=person)
	context = {'my_comments': my_comments}
	return render_to_response('mycomments.html', context, context_instance=RequestContext(request))	

def CommentsDelete(request, id):
	comm_del = get_object_or_404(Comment,id=id)
	comm_del.delete()
	return HttpResponseRedirect('/listnews/')

def detail_my_comms(request, id):
   comments = get_object_or_404(Comment,id=id)
   context = {'comments': comments}
   return render_to_response('detailmycomms.html', context, context_instance=RequestContext(request))

def show_foda(request):
    #foda = News.objects.all()
    #user = request.user.pk
	#person = Person.objects.get(user_id=user)
	news = News.objects.all()
	ratings_list_by_category={}
	foda = News.objects.all()
	fortaleza_news_max = foda.filter(category='Fortaleza').aggregate(Max('rating'))
	#fortaleza_news_max_1 = fortaleza_news_max.filter(category_in=[1,2])
	ratings_list_by_category['Fortaleza'] = fortaleza_news_max['rating__max']
	foda = News.objects.all()
	oportunidad_news_max = foda.filter(category='Oportunidad').aggregate(Max('rating'))
	#oportunidad_news_avg_1 = News.objects.filter(category='Oportunidad').aggregate(Avg('rating'))
	ratings_list_by_category['Oportunidad'] = oportunidad_news_max['rating__max']
	foda = News.objects.all()
	debilidad_news_max = foda.filter(category='Debilidad').aggregate(Max('rating'))
	#debilidad_news_avg_1 = News.objects.filter(category='Debilidad').aggregate(Avg('rating'))
	ratings_list_by_category['Debilidad'] = debilidad_news_max['rating__max']
	foda = News.objects.all()
	amenaza_news_max = foda.filter(category='Amenaza').aggregate(Max('rating'))
	#amenaza_news_avg_1 = News.objects.filter(category='Amenaza').aggregate(Avg('rating'))
	ratings_list_by_category['Amenaza'] = amenaza_news_max['rating__max']
	context = {'rating_list': ratings_list_by_category, 'news': news}
	return render_to_response('home.html', context, context_instance=RequestContext(request))

def detail_my_news(request, id):
   news = get_object_or_404(News,id=id)
   context = {'news': news}
   return render_to_response('detailmynews.html', context, context_instance=RequestContext(request))

def detail_news(request, id):
   news = get_object_or_404(News,id=id)
   context = {'news': news}
   return render_to_response('detailnews.html', context, context_instance=RequestContext(request))

def PersonRegistration(request):
   	if request.user.is_authenticated():
   		return HttpResponseRedirect('/profile/')
   	if request.method == 'POST':
   		form = RegistrationForm(request.POST)
   		if form.is_valid():
   			user = User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
   			user.save()
   			#person = user.get_profile()
   			#person.name = form.cleaned_data['name']
   			#person.birthday = form.cleaned_data['birthday']
   			#person.save()
   			person = Person(user=user, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], job_description=form.cleaned_data['job_description'])
   			person.save()
   			return HttpResponseRedirect('/profile/')
   		else:
   			return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
   	else:
   		''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form}
                return render_to_response('register.html', context, context_instance=RequestContext(request))

def LoginRequest(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			person = authenticate(username=username, password=password)
			if person is not None:
				login(request, person)
				return HttpResponseRedirect('/profile/')
			else:
				return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
		else:
			return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
	else:
		'''No esta ingresando el usuario'''
		form = LoginForm()
		context = {'form': form}
		return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/')

def edit_news(request, id):
	news_upd = get_object_or_404(News,id=id)
	#news_edit = {'news':news_upd}
	#news_all = News.objects.all()
	form = UpdateNewsForm(request.POST or None, instance=news_upd)
	if form.is_valid():
		#user = request.user.pk
		#person = Person.objects.get(user_id=user)
		#news = News(title=form.cleaned_data['title'],
		#		description=form.cleaned_data['description'],
		#		date=form.cleaned_data['date'],
		#		source=form.cleaned_data['source'],
		#		category=form.cleaned_data['category'],
		#	 	user=person)
		#news_upd = news
		form.save()
		return HttpResponseRedirect('/mynews/')
	else:
		form = UpdateNewsForm(news_upd)
	form = UpdateNewsForm()
	context = {'form': form}
	return render_to_response('updatenews.html', context, context_instance=RequestContext(request))


@login_required
def NewsCreate(request):
	#import ipdb; ipdb.set_trace()
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	if request.method == 'POST':
		form = NewsForm(request.POST)
		if form.is_valid():
			#person = Person.objects.filter(first_name=request.user)
			# user = User.objects.filter(username=request.user).values('id')
			# person = Person.objects.filter(user).values('id')
			# usr = Person.objects.get(person)
			user = request.user.pk
			person = Person.objects.get(user_id=user)
			news = News(title=form.cleaned_data['title'],
				description=form.cleaned_data['description'],
				date=form.cleaned_data['date'],
				source=form.cleaned_data['source'],
				category=form.cleaned_data['category'],
			 	rating=form.cleaned_data['rating'],
			 	user=person)
   			news.save()
   			#import ipdb; ipdb.set_trace()
   			return HttpResponseRedirect('/profile/')
   		else:
   			return render_to_response('news.html', {'form': form}, context_instance=RequestContext(request))
	else:
		'''No esta ingresando la noticia'''
		form = NewsForm()
		return render_to_response('news.html', {'form': form}, context_instance=RequestContext(request))

def NewsDelete(request, id):
	news_del = get_object_or_404(News,id=id)
	news_del.delete()
	return HttpResponseRedirect('/listnews/')


@login_required
def CommentCreate(request, id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			news = get_object_or_404(News,id=id)
			user = request.user.pk
			person = Person.objects.get(user_id=user)
			comment = Comment(description=form.cleaned_data['description'], date=form.cleaned_data['date'], user=person, news_item=news)
   			comment.save()
   			return HttpResponseRedirect('/listnews/')
   		else:
   			return render_to_response('comment.html', {'form': form}, context_instance=RequestContext(request))
	else:
		'''No esta ingresando el comentario'''
		form = CommentForm()
		return render_to_response('comment.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def Profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	#person = request.user.get_profile
	#context = {'person': person}
	#return render_to_response('profile.html', context, context_instance=RequestContext(request))
	#fortaleza_news = News.objects.filter(category='Fortaleza').aggregate(Avg('rating'))
	#rating = news['rating__avg']
	user = request.user.pk
	person = Person.objects.get(user_id=user)
	ratings_list_by_category={}
	fortaleza_news_avg = News.objects.filter(user_id=person)
	fortaleza_news_avg_1 = fortaleza_news_avg.filter(category='Fortaleza').aggregate(Avg('rating'))
	#fortaleza_news_avg_1 = News.objects.filter(category='Fortaleza').aggregate(Avg('rating'))
	ratings_list_by_category['Fortaleza'] = fortaleza_news_avg_1['rating__avg']
	oportunidad_news_avg = News.objects.filter(user_id=person)
	oportunidad_news_avg_1 = oportunidad_news_avg.filter(category='Oportunidad').aggregate(Avg('rating'))
	#oportunidad_news_avg_1 = News.objects.filter(category='Oportunidad').aggregate(Avg('rating'))
	ratings_list_by_category['Oportunidad'] = oportunidad_news_avg_1['rating__avg']
	debilidad_news_avg = News.objects.filter(user_id=person)
	debilidad_news_avg_1 = debilidad_news_avg.filter(category='Debilidad').aggregate(Avg('rating'))
	#debilidad_news_avg_1 = News.objects.filter(category='Debilidad').aggregate(Avg('rating'))
	ratings_list_by_category['Debilidad'] = debilidad_news_avg_1['rating__avg']
	amenaza_news_avg = News.objects.filter(user_id=person)
	amenaza_news_avg_1 = amenaza_news_avg.filter(category='Amenaza').aggregate(Avg('rating'))
	#amenaza_news_avg_1 = News.objects.filter(category='Amenaza').aggregate(Avg('rating'))
	ratings_list_by_category['Amenaza'] = amenaza_news_avg_1['rating__avg']
	context = {'rating_list': ratings_list_by_category}
	return render_to_response('profile.html', context, context_instance=RequestContext(request))