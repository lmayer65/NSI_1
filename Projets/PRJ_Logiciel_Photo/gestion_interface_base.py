############################################################
############## Fonctions utilitaires #######################
############################################################

# Met à jour les canevas après chaque modification d'image
def mise_a_jour_images():
    
    # Suppression des images précédentes
    if dict_tkinter["img_g"] is not None:
        dict_tkinter["canvas_g"].delete(dict_tkinter["img_g"])
        dict_tkinter["img_g"] = None

    if dict_tkinter["img_d"] is not None:
        dict_tkinter["canvas_d"].delete(dict_tkinter["img_d"])
        dict_tkinter["img_d"] = None
    
    # Mise à jour des nouvelles
    if image_gauche is not None:
        dict_tkinter["img_g"] = ImageTk.PhotoImage(image=image_gauche)
        dict_tkinter["id_img_g"] = dict_tkinter["canvas_g"].create_image(0, 0, image=dict_tkinter["img_g"], anchor=tk.NW)

    if image_droite is not None:
        dict_tkinter["img_d"] = ImageTk.PhotoImage(image=image_droite)
        dict_tkinter["id_img_d"] = dict_tkinter["canvas_d"].create_image(0, 0, image=dict_tkinter["img_d"], anchor=tk.NW)

        
# Charge une image du PC de l'utilisateur
# Inutile de la monter sur Jupyter
def ouvrir_fichier():
    global image_gauche
    filename = filedialog.askopenfilename(parent=root)
    img = Image.open(filename)
    image_gauche = img.copy()
    mise_a_jour_images()

    
# Applique un des filtres à l'image de gauche
def applique_filtre_gris() :
    global image_droite
    image_droite = filtre_gris(image_gauche)
    mise_a_jour_images()

    
########## AJOUTER LES APPLICATIONS A D'AUTRES FILTRES ICI  ############


########################################################################
    
    
# Création de l'interface et des boutons - action  
#######################  A MODIFIER ####################################
def creation_interface(root):
    
    root.title("Traitement images")
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=1)
    
    dict_tkinter["canvas_g"] = tk.Canvas(frame, width=512, height=512, background="grey")
    dict_tkinter["canvas_g"].pack(padx=8, pady=8, side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    panneau_boutons = tk.Frame(frame, background="blue")
    panneau_boutons.pack(side=tk.LEFT, fill=tk.X, expand=0)
    
    dict_tkinter["canvas_d"] = tk.Canvas(frame, width=512, height=512, background="grey")
    dict_tkinter["canvas_d"].pack(padx=8, pady=8, side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    # Eviter les caractères accentués !
    btn = tk.Button(panneau_boutons, text="Charger photo", command=ouvrir_fichier)
    btn.pack(fill=tk.X, expand=1)
    btn = tk.Button(panneau_boutons, text="Teintes de Gris", command=applique_filtre_gris)
    btn.pack(fill=tk.X, expand=1)
    