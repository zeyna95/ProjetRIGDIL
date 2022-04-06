from django.shortcuts import  render, redirect
import json
from .tree import Arbre_mot, calculAdjacent_mot, articles_mot, similariteArticle_mot, trouverClasses_mot
from .forms import NewUserForm, SearchForm
from .treeSemantique import Arbre, trouverClasses, similariteArticle, calculAdjacent, articles
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 

similarite = similariteArticle(articles)
adjacent = calculAdjacent(similarite)
ar = Arbre()
classes = trouverClasses(adjacent)
ar.add(classes,adjacent,similarite)
# Create your views here.

#pour mot clé
similarite_mot = similariteArticle_mot(articles_mot)
adjacent_mot = calculAdjacent_mot(similarite_mot)
classe_mot = trouverClasses_mot(adjacent_mot)
ar_mot = Arbre_mot()
ar_mot.add(classe_mot,adjacent_mot,similarite_mot)

def hello(request):
   return render(request, '/search/result.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('/login')
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

def search_request(request) :
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			search = form.cleaned_data.get('search')
			profil = form.cleaned_data.get('profil')
			if profil=="oui":
				user = request.user
				search = search + ' ' + user.pays + ' '+ user.matrimoniale + ' ' + user.profession + ' ' +  user.sexe
			te = ar_mot.classe_article(ar.root, search)
			tab_result = []
			tab_res = []
			for elt in reversed(te):
				if elt != te[0]:
					for res in elt:
						if res not in tab_result:
							with open("C:/Users/E450/Desktop/M2GDIL/ProjetRI/articles/"+res,encoding="utf8") as a :
								data = json.load(a)
							tab_result.append(res)
							data["nomArticle"] = res
							tab_res.append(data)
			messages.success(request, "Search successful." )
			return render(request=request,template_name='search/result.html',context = {'searchs':tab_res,
                                                                               'recherche':search})
	form = SearchForm()
	return render (request=request, template_name="search/accueil.html")

def view_detail(request,nomArticle):
    if request.method == "GET":
        with open("C:/Users/E450/Desktop/M2GDIL/ProjetRI/articles/"+nomArticle,encoding="utf8") as a :
            data = json.load(a)
        data["nomArticle"] = nomArticle
        return render (request=request, template_name="search/detail.html",context = {"detail":data})
    return render (request=request, template_name="search/accueil.html")