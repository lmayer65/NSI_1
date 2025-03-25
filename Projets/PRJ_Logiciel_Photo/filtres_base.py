############################################################
##################### Filtres ##############################
############################################################

def filtre_gris(img1):
    
    # Création d'une nouvelle image ayant les mêmes
    # dimensions que celle chargée
    img2 = Image.new("RGB",img1.size)
    
    for i in range(img2.size[0]):
        for j in range(img2.size[1]):
            
            rouge, vert, bleu = img1.getpixel((i,j))
              
            gris = int(rouge*0.299 + vert*0.587 + bleu*0.144) 
        
            img2.putpixel( (i,j),(gris,gris,gris) )
            
    return img2


############ AJOUTER LES AUTRES FILTRES APRES ##############
                       
                       
############################################################