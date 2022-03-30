import json
import numpy as np
from spacy.lang.fr import French
from spacy.lang.fr.stop_words import STOP_WORDS
from os import listdir
from graphviz import Digraph

# les mot vides 
# le debut des mots vides en majuscule
NEW_STOP_WORDS = [w.capitalize() for w in STOP_WORDS]

ponctuation = ['!','.',':','?',',','%','¨','+','=','"','<','>',' ']
MOT_VIDES = set(set(STOP_WORDS).union(NEW_STOP_WORDS)).union(ponctuation)

# recuperer le nom de tous les articles pour le premier dossier articlesprojet
def charger():
    fichiers = listdir('C:/Users/E450/Desktop/M2GDIL/ProjetRI/articles') 
    # un dico d'article contenant tous les articles
    articles = {}
    for nomArticle in fichiers :
        with open("C:/Users/E450/Desktop/M2GDIL/ProjetRI/articles/"+nomArticle,encoding="utf8") as a :
            data = json.load(a)
        motCle = [word for word in data['contenuArticle'].split() if word not in MOT_VIDES]
        if motCle :
            articles[nomArticle] = motCle
    return articles
articles = charger()
#print(articles)

# matrice de similarité 
def similariteArticle(articles):
    similariteArticle = {}
    for nomArticle1 in articles.keys() :
        row = {}
        for nomArticle2 in articles.keys() :
            #print(nomArticle1+"  "+nomArticle2)
            intersectionArticle = len(set(articles[nomArticle1]).intersection(set(articles[nomArticle2])))
            unionArticle = len(set(articles[nomArticle1]).union(set(articles[nomArticle2])))
            row[nomArticle2]  = round(intersectionArticle/unionArticle,4)
        similariteArticle[nomArticle1] = row
    return similariteArticle
    # fini pour la matrice de similarité des articles
similarite = similariteArticle(articles)

def graphSansEli(similarite):
    g = Digraph('G', filename='arbre.pdf')
    for nomArticle in similarite :
            max = 0
            for nomArticle1 in similarite :
                if(nomArticle!=nomArticle1):
                    simi = similarite[nomArticle][nomArticle1]
                    if(simi>max):
                        max = simi
                        nomArticleMax = nomArticle1
            g.edge(nomArticle[7:-5], nomArticleMax[7:-5],label = str(max))
    return g

def calculAdjacent(similarite):

    # adjacent est la matrice d'adjacent initiale de tous les articles
    adjacent = {}
    i = 0
    for nomArticle in similarite :

        adjacent[nomArticle] = {}
        max = 0
        for nomArticle1 in similarite :
            adjacent[nomArticle][nomArticle1] = 0
            if(nomArticle!=nomArticle1):
                simi = similarite[nomArticle][nomArticle1]
                if(simi>max):
                    max = simi
                    nomArticleMax = nomArticle1
        adjacent[nomArticle][nomArticleMax] = 1

    for art in adjacent:
        for art1 in adjacent[art]:
            if adjacent[art1][art] == 1:
                adjacent[art][art1] = 1
    return adjacent
adjacent = calculAdjacent(similarite)

def determinerConnexite(adjacent):
    T = {}
    i=0
    for a in adjacent :
        T[a] = i
        i=i+1
    modifications = True
    while modifications:
        modifications = False
        for art in adjacent:
            for art1 in adjacent[art] :
                if adjacent[art][art1] == 1 and T[art] != T[art1]:
                    T[art] = T[art1] = min(T[art], T[art1])
                    modifications = True
    
    return T

def trouverClasses(adjacent):
        cnx = determinerConnexite(adjacent)
        classes = {}
        k =  0
        for i, c in cnx.items():
            if c not in classes:
                classes[c] = []
            classes[c].append(i)
        return classes

# pour touver la valuer de la similarité minimum et eliminer le l'article de la classe
def adjacentFils(noeud,adjacentMax,similariteArticle):
    min = 2
    dico = {}
    minA1 = ""
    minA2 =""
    for conts in noeud.contenu :
        for cont in conts :
            dico[cont] = {}
            for c in conts :
                if(adjacentMax[cont][c]==1):
                    dico[cont][c]=1
                    k = similariteArticle[cont][c]
                    if k < min :
                        minA1 = cont
                        minA2 = c
                        min = k
                else :
                    dico[cont][c]=0
    dico[minA1][minA2] = 0
    dico[minA2][minA1] = 0
    return dico

# la classe pour contruire un noeud
class Node:
    def __init__(self,val):
        self.contenu =[]
        self.fils = None
        self.val = val 

class Arbre:
    def __init__(self):
        self.root = None
        self.simi = {}
    def add(self, classes,adjacentMax,similariteArticle) :
        if(self.root==None):
            self.root = Node('C')
            self.root.fils = []
            self.simi[self.root.val] = {}
            for key,cl in classes.items():
                row = Node(str(self.root.val)+'-'+str(key))
                self.simi[self.root.val][row.val] = 1
                row.contenu = cl
                for k in classes[key]:
                    self.root.contenu.append(k)
                self.root.fils.append(row)
            for r in self.root.fils:
                adjFils = self._adjacentFils(r,adjacentMax,similariteArticle)
                if(adjFils!=None):
                    classe = self._trouverClasses(adjFils)
                    self._add(classe,r,adjacentMax,similariteArticle)

    def _add(self, classes, noeud,adjacentMax,similariteArticle):
        if(len(noeud.contenu)!=1):
            noeud.fils = []
            self.simi[noeud.val] = {}
            for key,cl in classes.items():
                if(len(cl)==1):
                    row = Node(cl[0][7:-5])
                else:
                    row = Node(str(noeud.val)+'-'+str(key))
                self.simi[noeud.val][row.val] = 1
                row.contenu = cl
                for k in classes[key]:
                    noeud.contenu.append(k)
                noeud.fils.append(row)
            for r in noeud.fils:
                adjFils = self._adjacentFils(r,adjacentMax,similariteArticle)
                if(adjFils!=None):
                    classe = self._trouverClasses(adjFils)
                    self._add(classe,r,adjacentMax,similariteArticle)

    def _adjacentFils(self,noeud,adjacentMax,similariteArticle):
        min = 2
        dico = {}
        minA1 = " "
        minA2 =" "
        parent = {}
        if(len(noeud.contenu)!=1):
            for cont in noeud.contenu :
                dico[cont] = {}
                parent[cont] = {}
                for c in noeud.contenu :
                    if(adjacentMax[cont][c]==1):
                        dico[cont][c]=1
                        k = similariteArticle[cont][c]
                        if k < min :
                            minA1 = cont
                            minA2 = c
                            min = k
                            parent[cont][c] = k
                    else :
                        dico[cont][c]=0
            for cle, val in parent.items():
                for i in val :
                    if(min == parent[cle][i]):
                        dico[cle][i] = 0
                        dico[i][cle] = 0
                        
            
            return dico
        else:
            return None

    def _determinerConnexite(self,adjacent):
        T = {}
        i=0
        for a in adjacent :
            T[a] = i
            i=i+1
        modifications = True
        while modifications:
            modifications = False
            for art in adjacent:
                for art1 in adjacent[art] :
                    if adjacent[art][art1] == 1 and T[art] != T[art1]:
                        T[art] = T[art1] = min(T[art], T[art1])
                        modifications = True

        return T

    def _trouverClasses(self,adjacent):
        cnx = self._determinerConnexite(adjacent)
        classes = {}
        k =  0
        for i, c in cnx.items():
            if c not in classes:
                classes[c] = []
            classes[c].append(i)
        return classes
    
    def affichArbre(self) :
        if(self.root != None):
            self._affiche(self.root)

    def _affiche(self,noeud):
        print(noeud.val)
        if(len(noeud.contenu)==1):
            print(noeud.contenu[0])
        else:
            print(noeud.contenu)
        if(noeud.fils):
            for c in noeud.fils:
                self._affiche(c)
    
    def _simi_article(self,motCle,neoud):
        simi = 0;
        for art in neoud.contenu:
            intersectionArticle = len(set(motCle).intersection(set(articles[art])))
            unionArticle = len(set(motCle).union(set(articles[art])))
            n  = round(intersectionArticle/unionArticle,4)
            if(n>=simi):
                simi = n
        return simi

    def _determiner_mot_cle(self,article):
        with open("C:/Users/E450/Desktop/M2GDIL/ProjetRI/articlesTest/"+article,encoding="utf8") as a :
            data = json.load(a)
        motCle = [word for word in data['contenuArticle'].split() if word not in MOT_VIDES]
        return motCle
    
    def _recur(self,noeud,motCle,classe_art):
        sim_max = 0;
        num_fils = -1
        if(noeud.fils==None):
            return noeud.contenu,classe_art,noeud.val
        classe_art = noeud.val
        for num, key in enumerate(noeud.fils):
            a = self._simi_article(motCle,key)
            if(a>=sim_max):
                sim_max = a
                num_fils = num
        return self._recur(noeud.fils[num_fils],motCle,classe_art)
    
    def classe_article(self,root,article):
        
        mot_cle = self._determiner_mot_cle(article)
        cont , classe, art = self._recur(self.root,mot_cle,root.val)
        return mot_cle, cont , classe, art
         
                
    def tracerGraphe(self):
        g = Digraph('G', filename='arbre.pdf')
        for c,cl in self.simi.items():
            for i in cl:
                if(self.simi[c][i]==1):
                    g.edge(c, i)
        return g
        
