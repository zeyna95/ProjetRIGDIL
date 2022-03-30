from django.shortcuts import  render, redirect
from .forms import NewUserForm, SearchForm
from .treeSemantique import Arbre, trouverClasses, similariteArticle, calculAdjacent, articles
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 


# Create your views here.

def hello(request):
   return render(request, 'search/result.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('/accueil')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="search/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('/accueil')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="search/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/login')

def search_request(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			search = form.cleaned_data.get('search')
			print(search)
			similarite = similariteArticle(articles)
			adjacent = calculAdjacent(similarite)
			ar = Arbre()
			classes = trouverClasses(adjacent)
			ar.add(classes,adjacent,similarite)
			te = ar.classe_article(ar.root, search)
			print(te)
			messages.success(request, "Search successful." )
			return redirect('result', searchs=search)
	form = SearchForm()
	return render (request=request, template_name="search/accueil.html")