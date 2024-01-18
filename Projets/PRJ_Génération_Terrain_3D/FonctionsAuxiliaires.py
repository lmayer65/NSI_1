from math import pow,sqrt
from random import randint
from random import random
from time import time
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D



###########################################################################################################
############################################### Algorithme de Perlin #######################################
###########################################################################################################


# Interpolation classique linéaire
def interpolationLinéaire(val1, val2, n, ecart) :
    if n!=0 :
        return val1 + ecart*(val2-val1)/n
    else :
        return val1


# Interpolation cubique
def interpolationCubique(val1, val2, n, ecart) :
    if n==0 :
        return val1
    if n==1 :
        return val2
    a = float(ecart/n);
    v1 = 3*pow(1-a, 2) - 2*pow(1-a,3);
    v2 = 3*pow(a, 2) - 2*pow(a, 3);
    return val1*v1 + val2*v2;


# Calcule l'altitude aux coordonnées par rapport aux bornes
def doubleInterpolation(i,j,taille,freqCour,tBaseCalque,choixCubique) :

    # Détermination des bornes
    pas = int(taille/freqCour);

    # Bornes en abscisses
    q = int(i/pas)
    xMin = q*pas
    xMax = (q + 1)*pas

    # Attention à ne pas dépasser le terrain
    if xMax >= taille :
        xMax = taille - 1

    # Bornes en ordonnées
    q = int(j/pas)
    yMin = q*pas
    yMax = (q + 1)*pas

    # Attention à ne pas dépasser le terrain
    if yMax >= taille :
        yMax = taille - 1

    # Récupération des valeurs aléatoires aux bornes
    val00 = tBaseCalque[xMin][yMin]
    val01 = tBaseCalque[xMin][yMax]
    val10 = tBaseCalque[xMax][yMin]
    val11 = tBaseCalque[xMax][yMax]
    valeurInferieure = interpolationLinéaire(val00, val01, yMax - yMin, j - yMin)
    valeurSuperieure  = interpolationLinéaire(val10, val11, yMax - yMin, j - yMin)
    if choixCubique :
        valeurFinale = interpolationCubique(valeurInferieure, valeurSuperieure, xMax - xMin , i - xMin)
    else:
        valeurFinale = interpolationLinéaire(valeurInferieure, valeurSuperieure, xMax - xMin , i - xMin)
    return valeurFinale



def calculSommePersistance(nombreOctaves,persistanceInitiale):
    
    sommePersistance=0
    persistanceCourante = persistanceInitiale
    
    for n in range(0,nombreOctaves) :
        sommePersistance += persistanceCourante
        persistanceCourante *= persistanceInitiale
        
    return sommePersistance



def generationCalques(nombreOctaves,tailleTerrain):
    
    tabCalques=[]
    
    for n in range(0,nombreOctaves) :
        calque = [[0 for i in range(0,tailleTerrain)] for j in range(0,tailleTerrain)]
        tabCalques.append(calque)
        
    return tabCalques



def ajoutCalques(tailleTerrain,persistanceInitiale,nombreOctaves,tabCalques,sommePersistance):
    
    tabDefinitifCalque = [[0 for i in range(0,tailleTerrain)] for j in range(0,tailleTerrain)]
    persistanceCourante = persistanceInitiale
    
    for i in range(0,tailleTerrain) :
        for j in range(0,tailleTerrain) :
            for n in range(0,nombreOctaves) :
                tabDefinitifCalque[i][j] += tabCalques[n][i][j]*persistanceCourante
                persistanceCourante *= persistanceInitiale
            # Normalisation
            tabDefinitifCalque[i][j] =  tabDefinitifCalque[i][j] / sommePersistance;
            persistanceCourante = persistanceInitiale
    
    return tabDefinitifCalque



def remplissageCalques(nombreOctaves,tailleTerrain,tabBaseCalque,frequenceInitiale,tabCalquesTemp,choixCubique):
    
    frequenceCourante = frequenceInitiale
    for n in range(0,nombreOctaves) :
        for i in range(0,tailleTerrain) :
            for j in range(0,tailleTerrain):
                valeur = doubleInterpolation(i,j,tailleTerrain,frequenceCourante,tabBaseCalque,choixCubique)
                tabCalquesTemp[n][i][j] = valeur
        frequenceCourante *= 2
    
    return tabCalquesTemp



def creationCalqueDefinitif(nombreOctaves,tailleTerrain,frequenceInitiale,tabBaseCalque,
                            persistanceInitiale,choixCubique):
    
    tabCalquesTemp = generationCalques(nombreOctaves,tailleTerrain)
    tabCalques = remplissageCalques(nombreOctaves,tailleTerrain,tabBaseCalque,
                                    frequenceInitiale,tabCalquesTemp,choixCubique)
    persistanceCourante = persistanceInitiale
    sommePersistance = calculSommePersistance(nombreOctaves,persistanceInitiale)
    tabDefinitifCalque = ajoutCalques(tailleTerrain,persistanceInitiale,nombreOctaves,tabCalques,sommePersistance)
    
    return tabDefinitifCalque

    
###########################################################################################################
############################################### Algorithme DS #############################################
###########################################################################################################

def EtapeDiamant(iAbs, iOrd, demiEspacement,tailleTerrain,tabValeurs) :
    
    somme = 0.0
    compteur = 0
  

    if (iAbs >= demiEspacement)  and  (iOrd >= demiEspacement) : 
        somme += tabValeurs[iAbs-demiEspacement][iOrd-demiEspacement] 
        compteur += 1

    if (iAbs >= demiEspacement)  and (iOrd + demiEspacement < tailleTerrain) :
        somme += tabValeurs[iAbs-demiEspacement][iOrd+demiEspacement]
        compteur += 1 

    if (iAbs + demiEspacement <  tailleTerrain)  and (iOrd >= demiEspacement) : 
        somme += tabValeurs[iAbs+demiEspacement][iOrd-demiEspacement] 
        compteur += 1

    if (iAbs + demiEspacement <  tailleTerrain)  and (iOrd + demiEspacement < tailleTerrain) :
        somme += tabValeurs[iAbs+demiEspacement][iOrd+demiEspacement] 
        compteur += 1

    return somme / compteur



def EtapeCarre(iAbs, iOrd, demiEspacement,tailleTerrain,tabValeurs) :
    
    somme = 0.0
    compteur = 0
  

    if iAbs >= demiEspacement : 
        somme += tabValeurs[iAbs-demiEspacement][iOrd] 
        compteur += 1
 
    if iAbs + demiEspacement < tailleTerrain : 
        somme += tabValeurs[iAbs+demiEspacement][iOrd]
        compteur += 1

    if iOrd >= demiEspacement :
        somme += tabValeurs[iAbs][iOrd-demiEspacement] 
        compteur += 1
 
    if iOrd + demiEspacement < tailleTerrain :
        somme += tabValeurs[iAbs][iOrd+demiEspacement] 
        compteur += 1

    return somme / compteur



def creationTerrain(tailleTerrain,tabValeurs,variabilite) :
    
    espacement = tailleTerrain - 1
    
    while espacement > 1 :  
        
        demiEspacement = int(espacement / 2)
    
        # Etape du diamant 
        for iAbs in range(demiEspacement,tailleTerrain,espacement) :
            for iOrd in range(demiEspacement,tailleTerrain,espacement) :
                # La hauteur prise est la moyenne de celles des 4 bornes (fonction) et une variation aléatoire
                tabValeurs[iAbs][iOrd] = EtapeDiamant(iAbs, iOrd, demiEspacement,tailleTerrain,tabValeurs) + 0.2*espacement*(random()-0.5)*variabilite 
 
        # Etape du carré 
        for iAbs in range(0,tailleTerrain,demiEspacement) :
            if not (iAbs/demiEspacement)% 2 :
                iOrdStart = demiEspacement 
            else :
                iOrdStart = 0
                
            for iOrd in range(iOrdStart,tailleTerrain,espacement) :
                # La hauteur prise est la moyenne de celles des 4 bornes (fonction) et une variation aléatoire
                tabValeurs[iAbs][iOrd] = EtapeCarre(iAbs, iOrd, demiEspacement,tailleTerrain,tabValeurs) + 0.2*espacement*(random()-0.5)*variabilite

 
        # Division de la partie de la carte utilisée par deux
        espacement = demiEspacement
     
    return tabValeurs


###########################################################################################################
################################ Fonctions Python pour l'image, l'affichage etc.###########################
######################################   Ne pas modifier    ###############################################

def remplissageZ(tailleTerrain,tabDefinitifCalque,Z):

    for i in range(0,tailleTerrain) :
        for j in range(0,tailleTerrain) :
            Z[i][j] = tabDefinitifCalque[i][j]


# Affichage du terrain
def affichageTerrain(tailleTerrain,tabDefinitifCalque,hauteurMaximale) :
    
    # Partie affichage de Python
    X = np.arange(0,tailleTerrain,1)
    Y = np.arange(0,tailleTerrain,1)
    X, Y = np.meshgrid(X, Y)
    Z = X + Y

    #Remplissage du Z
    remplissageZ(tailleTerrain,tabDefinitifCalque,Z)

    fig = plt.figure(figsize = (50,50))
    ax = fig.gca(projection='3d')
    ax.set_zlim(-hauteurMaximale, 2*hauteurMaximale)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    terrain = ax.plot_surface(X, Y, Z, cmap=plt.cm.gist_earth,linewidth=0, antialiased=False)
    fig.colorbar(terrain, shrink=0.1, aspect=5)
    plt.show()
    

# Affiche une image
def affichageImage(image) :
    
    plt.plot(1,1,1)
    plt.imshow(image,cmap = "gray")

    
    
# Construction de l'image à partir des données du tableau double
def constructionImage(tailleTerrain,tabValeurs,hauteurMaximale) :
    img=Image.new('L',(tailleTerrain,tailleTerrain))
    
    for i in range (0,tailleTerrain):
        for j in range(0,tailleTerrain):
            m=int(float(tabValeurs[tailleTerrain-j-1][i])*255.0/float(hauteurMaximale))
            img.putpixel((i,j),m)
        
    return img
    
    
    
# Affichage de l'image représentant les hauteurs et du terrain lui correspondant
def affichageImageTerrain(tailleTerrain,tabValeurs,hauteurMaximale,image) :
    
    # Partie 3D du terrain
    X = np.arange(0,tailleTerrain,1)
    Y = np.arange(0,tailleTerrain,1)
    X, Y = np.meshgrid(X, Y)
    Z = X + Y

    # Remplissage du Z
    remplissageZ(tailleTerrain,tabValeurs,Z)

    fig = plt.figure(figsize = (20,20))
    
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Carte des hauteurs")
    plt.imshow(image,cmap="gray")
    
    ax = fig.add_subplot(2, 1, 2, projection='3d')
    plt.title("Terrain généré")
    ax.set_zlim(-hauteurMaximale/2, hauteurMaximale)  # Valeurs extrêmes empiriques
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    terrain = ax.plot_surface(X, Y, Z, cmap=plt.cm.gist_earth,linewidth=0, antialiased=False)
    fig.colorbar(terrain, shrink=0.1, aspect=5)
    plt.show()

def tempsMoyen(nombreDeTerrains,tailleTerrain,nombreOctaves,frequenceInitiale,tabBaseCalque,
           persistanceInitiale,choixInterpolationCubique):
    if nombreDeTerrains==1:
        temps=time()
        tabDefinitifCalque = creationCalqueDefinitif(nombreOctaves,tailleTerrain,frequenceInitiale,tabBaseCalque,
                                                     persistanceInitiale,choixInterpolationCubique)
        temps = (time()-temps)
        print("Le temps de génération d'un terrain",tailleTerrain,"*",tailleTerrain,"avec l'algorithme de Perlin est de :",temps)
    else :
        moyenne=0.0
        for i in range (nombreDeTerrains):
            temps = time()
            tabDefinitifCalque = creationCalqueDefinitif(nombreOctaves,tailleTerrain,frequenceInitiale,tabBaseCalque,
                                                         persistanceInitiale,choixInterpolationCubique)
            temps = (time()-temps)
            moyenne+=temps
            print("Exécution n°",i+1,": temps passé :",temps,"secondes")
        print("Le temps de génération moyen de",nombreDeTerrains,"terrains",tailleTerrain,"*",tailleTerrain,
              "avec l'algorithme de Perlin est de :",moyenne/nombreDeTerrains,"secondes")
        
###########################################################################################################