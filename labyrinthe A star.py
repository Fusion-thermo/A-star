from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import numpy as np
import os
from time import time, sleep


hauteur, largeur=500, 500
cote_depart=20
nombre_clic_droit=0
laby=False


def quadrillage(coter=cote_depart):
	global cote, grille, l_grille, L_grille,nombre_clic_droit,laby
	Canevas.delete(ALL)
	cote=int(coter)
	for i in range((hauteur-int(cases_hauteur.get()))//cote):
		for j in range((largeur-int(cases_largeur.get()))//cote):
			Canevas.create_rectangle(cote*j, cote*i, cote*j+cote, cote*i+cote)
	grille=np.ones(((hauteur-int(cases_hauteur.get()))//cote, (largeur-int(cases_largeur.get()))//cote))
	l_grille=(hauteur-int(cases_hauteur.get()))//cote-1
	L_grille=(largeur-int(cases_largeur.get()))//cote-1
	nombre_clic_droit=0

def restaurer():
	for x in range(L_grille+1):
		for y in range(l_grille+1):
			if grille[y,x]==1:
				Canevas.create_rectangle(x*cote, y*cote, x*cote+cote, y*cote+cote, fill="white")

def Clic_gauche(event):
	global x_clic, y_clic
	x_clic=event.x
	y_clic=event.y
	if laby==False:
		x=(event.x//cote)*cote
		y=(event.y//cote)*cote
		if -1<event.y//cote<l_grille+1 and -1<event.x//cote<L_grille+1:
			if grille[event.y//cote, event.x//cote]==100:
				Canevas.create_rectangle(x, y, x+cote, y+cote, fill="white")
				grille[event.y//cote, event.x//cote]=1
			else:
				Canevas.create_rectangle(x, y, x+cote, y+cote, fill="black")
				grille[event.y//cote, event.x//cote]=100

def Clic_droit_survol(event):
	global x_clic, y_clic, cote
	x_clic=event.x
	y_clic=event.y
	x=(event.x//cote)*cote
	y=(event.y//cote)*cote
	if -1<event.y//cote<l_grille+1 and -1<event.x//cote<L_grille+1:
		if grille[event.y//cote, event.x//cote]==1:
			Canevas.create_rectangle(x, y, x+cote, y+cote, fill="black")
			grille[event.y//cote, event.x//cote]=100


def Clic_gauche_laby(event):
	global cote
	Canevas.create_rectangle(x_clic,y_clic,event.x,y_clic+(event.x-x_clic),outline='red')	
	cote=abs(event.x-x_clic)

def Clic_gauche_release(event):
	if event.x != x_clic or event.y != y_clic:
		a=(event.y-y_clic)/(event.x-x_clic+0.000001)
		b=y_clic-a*x_clic
		sens=int((event.x-x_clic)//(abs(event.x-x_clic+0.000001)))
		if sens==0:
			sens=1
		for x1 in range(x_clic,event.x,sens):
			y1=a*x1+b
			x=(x1//cote)*cote
			y=(y1//cote)*cote
			if -1<y1//cote<l_grille+1 and -1<x1//cote<L_grille+1:
				Canevas.create_rectangle(x, y, x+cote, y+cote, fill="black")
				grille[int(y1//cote), int(x1//cote)]=100

def Clic_droit(event):
	global nombre_clic_droit,x_depart, y_depart,x_arrivee, y_arrivee
	x=(event.x//cote)*cote
	y=(event.y//cote)*cote
	if -1<event.y//cote<l_grille+1 and -1<event.x//cote<L_grille+1:
		if nombre_clic_droit==0:
			Canevas.create_rectangle(x, y, x+cote, y+cote, fill="green")
			nombre_clic_droit+=1
			grille[event.y//cote, event.x//cote]=-1
			x_depart, y_depart=event.y//cote, event.x//cote
		elif nombre_clic_droit==1:
			Canevas.create_rectangle(x, y, x+cote, y+cote, fill="red")
			nombre_clic_droit+=2
			grille[event.y//cote, event.x//cote]=-1
			x_arrivee, y_arrivee=event.y//cote, event.x//cote

def astar():
	global liste_dessin, closedlist
	debut_temps=time()
	code_en_cours=0
	#on utilise la distance de manhattan, càd la norme 1
	#structure du tuple : (qualité,x,y,code perso, code du parent)
	#avec qualité : distance au noeud parent(poids du noeud dans grille) + distance a noeud d'arrivée (norme 1) 
	openlist=[(0+abs(x_arrivee-x_depart)+abs(y_arrivee-y_depart),x_depart,y_depart,0,code_en_cours)]
	closedlist=[]
	liste_dessin=[]
	if value.get()=="1":
		coos_voisin_x=[0,1,1,1,0,-1,-1,-1]
		coos_voisin_y=[-1,-1,0,1,1,1,0,-1]
	else:
		coos_voisin_x=[0,1,0,-1]
		coos_voisin_y=[-1,0,1,0]

	noeud_courant=min(openlist)

	while noeud_courant[1]!=x_arrivee or noeud_courant[2]!=y_arrivee:
		#os.system("pause")
		if len(openlist)==0:
			break
		noeud_courant=min(openlist)
		openlist.remove(noeud_courant)
		closedlist.append(noeud_courant)
		liste_dessin.append((noeud_courant[1],noeud_courant[2],"orange"))
		#Canevas.create_rectangle(noeud_courant[2]*cote,noeud_courant[1]*cote, noeud_courant[2]*cote+cote, noeud_courant[1]*cote+cote, fill="orange")
		for i in range(len(coos_voisin_x)):
			suivant=False
			
			#hors de la matrice
			if noeud_courant[1]+coos_voisin_x[i]<0 or noeud_courant[1]+coos_voisin_x[i]>l_grille or noeud_courant[2]+coos_voisin_y[i]<0 or noeud_courant[2]+coos_voisin_y[i]>L_grille:
				continue
			
			#obstacle
			if grille[noeud_courant[1]+coos_voisin_x[i],noeud_courant[2]+coos_voisin_y[i]]==100:
				continue
			
			#dans la liste fermée
			for noeud in closedlist:
				if noeud[1]==noeud_courant[1]+coos_voisin_x[i] and noeud[2]==noeud_courant[2]+coos_voisin_y[i]:
					suivant=True
					break
			if suivant:
				continue
			suivant=False
			
			code_en_cours+=1

			#dans la liste ouverte, si oui on recalcule la qualité, si elle est meilleure on la met à jour et son parent aussi
			for noeud in openlist:
				if noeud[1]==noeud_courant[1]+coos_voisin_x[i] and noeud[2]==noeud_courant[2]+coos_voisin_y[i]:
					if noeud[0]>grille[noeud_courant[1]+coos_voisin_x[i],noeud_courant[2]+coos_voisin_y[i]]+abs(x_arrivee-noeud_courant[1]-coos_voisin_x[i])+abs(y_arrivee-noeud_courant[2]-coos_voisin_y[i]):
						maj_noeud=(grille[noeud_courant[1]+coos_voisin_x[i],noeud_courant[2]+coos_voisin_y[i]]+abs(x_arrivee-noeud_courant[1]-coos_voisin_x[i])+abs(y_arrivee-noeud_courant[2]-coos_voisin_y[i]),noeud_courant[1]+coos_voisin_x[i],noeud_courant[2]+coos_voisin_y[i],noeud[3],noeud_courant[3])
						openlist.remove(noeud)
						openlist.append(maj_noeud)
					suivant=True
					break
			if suivant:
				continue
			 #si rien de tout ça : on l'ajoute dans la liste ouverte
			openlist.append((grille[noeud_courant[1]+coos_voisin_x[i],noeud_courant[2]+coos_voisin_y[i]]+abs(x_arrivee-noeud_courant[1]-coos_voisin_x[i])+abs(y_arrivee-noeud_courant[2]-coos_voisin_y[i]),noeud_courant[1]+coos_voisin_x[i],noeud_courant[2]+coos_voisin_y[i],code_en_cours,noeud_courant[3]))
			liste_dessin.append((openlist[-1][1],openlist[-1][2],"blue"))
			#Canevas.create_rectangle((noeud_courant[2]+coos_voisin_y[i])*cote,(noeud_courant[1]+coos_voisin_x[i])*cote, (noeud_courant[2]+coos_voisin_y[i])*cote+cote, (noeud_courant[1]+coos_voisin_x[i])*cote+cote, fill="blue")
	

	if len(openlist)==0 and (noeud_courant[1]!=x_arrivee or noeud_courant[2]!=y_arrivee):
		conclusion=Label(fenetre,text="Pas de chemin possible")
		conclusion.pack()
	else:
		conclusion=Label(fenetre,text="Chemin trouvé.")
		conclusion.pack()
		x=x_arrivee
		y=y_arrivee
		parent=noeud_courant[4]
		liste_dessin.append((x,y,"green"))
		#Canevas.create_rectangle(y*cote,x*cote, y*cote+cote, x*cote+cote, fill="green")
		while parent!=0:
			i=0
			while closedlist[i][3]!=parent:
				i+=1
			x=closedlist[i][1]
			y=closedlist[i][2]
			parent=closedlist[i][4]
			liste_dessin.append((closedlist[i][1],closedlist[i][2],"green"))
			#Canevas.create_rectangle(y*cote,x*cote, y*cote+cote, x*cote+cote, fill="green")
		#Canevas.create_rectangle(y_depart*cote,x_depart*cote, y_depart*cote+cote, x_depart*cote+cote, fill="green")
		liste_dessin.append((x_depart,y_depart,"green"))
	
	temps = Label(fenetre, text=str(time()-debut_temps)+" s")
	temps.pack()

	dessin()

def dessin():
	recursif = fenetre.after(10,dessin)
	if liste_dessin!=[]:
		Canevas.create_rectangle(liste_dessin[0][1]*cote,liste_dessin[0][0]*cote, liste_dessin[0][1]*cote+cote, liste_dessin[0][0]*cote+cote, fill=liste_dessin[0][2])
		liste_dessin.remove(liste_dessin[0])
	else:
		fenetre.after_cancel(recursif)

def Ouvrir():
	global laby, hauteur, largeur, photo
	laby=True
	Canevas.delete(ALL)
	filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'),('all files','.*')])
	photo = PhotoImage(file=filename)
	pngdict[filename] = photo  # référence
	Canevas.create_image(0,0,anchor=NW,image=photo)
	Canevas.config(height=photo.height(),width=photo.width())
	hauteur=photo.height()
	largeur=photo.width()
	fenetre.title("Image "+str(photo.width())+" x "+str(photo.height()))
	Canevas.unbind('<B3-Motion>')
	Canevas.unbind('<ButtonRelease-1>')
	Canevas.unbind('<Button-3>')
	Canevas.bind('<ButtonRelease-1>',  Clic_gauche_laby)
	Canevas.bind('<Button-3>',  laby_vers_grille)

def laby_vers_grille(event):
	global cote, grille, l_grille, L_grille,nombre_clic_droit,hauteur, largeur, laby
	
	Canevas.unbind('<ButtonRelease-1>')
	Canevas.unbind('<Button-3>')
	Canevas.bind('<B3-Motion>',  Clic_droit_survol)
	Canevas.bind('<ButtonRelease-1>',  Clic_gauche_release)
	Canevas.bind('<Button-3>',  Clic_droit)

	grille=np.ones((hauteur//cote, largeur//cote))
	l_grille=hauteur//cote-1
	L_grille=largeur//cote-1
	for i in range(hauteur//cote):
		for j in range(largeur//cote):
			#Canevas.create_rectangle(cote*j, cote*i, cote*j+cote, cote*i+cote)
			if sum(photo.get(cote*j+cote//2,cote*i+cote//2))<3*245:
				grille[i,j]=100
	Canevas.delete(ALL)
	for i in range(hauteur//cote):
		for j in range(largeur//cote):
			if grille[i,j]==100:
				Canevas.create_rectangle(cote*j, cote*i, cote*j+cote, cote*i+cote,fill='black')
	
	
	nombre_clic_droit=0
	laby=False

fenetre=Tk()

Canevas=Canvas(fenetre, height=hauteur, width=largeur)
Canevas.pack(side=LEFT)

densite=StringVar()
densite.set(20)
echelle_cases_densite=Scale(fenetre,  orient='horizontal',  from_=7,  to=hauteur//2,  resolution=10,  \
tickinterval=100,  label='Densité',  variable=densite,  command=quadrillage)
echelle_cases_densite.pack(side="top")

cases_hauteur=StringVar()
cases_hauteur.set(0)
echelle_cases_hauteur=Scale(fenetre,  orient='horizontal',  from_=0,  to=hauteur,  resolution=10,  \
tickinterval=200,  label='Hauteur cases',  variable=cases_hauteur,  command=quadrillage)
echelle_cases_hauteur.pack(side="top")

cases_largeur=StringVar()
cases_largeur.set(0)
echelle_cases_largeur=Scale(fenetre,  orient='horizontal',  from_=0,  to=largeur,  resolution=10,  \
tickinterval=300,  label='largeur cases',  variable=cases_largeur,  command=quadrillage)
echelle_cases_largeur.pack(side="top")

value=StringVar()
value.set(1)
Choix1=Radiobutton(fenetre, text="Déplacement avec diagonales",variable=value, value=1)
Choix2=Radiobutton(fenetre, text="Déplacement sans diagonales",variable=value, value=2)
Choix1.pack()
Choix2.pack()

Bouton_astar = Button(fenetre,  text = 'Départ A*',  command = astar)
Bouton_astar.pack()

detruire_chemin1 = Button(fenetre,  text = 'Restaurer cette configuration',  command = restaurer)
detruire_chemin1.pack()

detruire_chemin2 = Button(fenetre,  text = 'Tout restaurer',  command = quadrillage)
detruire_chemin2.pack()

Canevas.bind('<Button-1>',  Clic_gauche)
Canevas.bind('<B3-Motion>',  Clic_droit_survol)
Canevas.bind('<ButtonRelease-1>',  Clic_gauche_release)
Canevas.bind('<Button-3>',  Clic_droit)

Bouton1 = Button(fenetre,  text = 'Quitter',  command = fenetre.destroy)
Bouton1.pack(side="bottom")


menubar = Menu(fenetre)
menufichier = Menu(menubar,tearoff=0)
menufichier.add_command(label="Ouvrir une image",command=Ouvrir)
menubar.add_cascade(label="Fichier", menu=menufichier)

fenetre.config(menu=menubar)

pngdict={}

quadrillage()

fenetre.mainloop()