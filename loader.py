# -*- coding: utf-8 -*-

import sys
import os
import maya.cmds as cmds
import importlib

# --- CONFIGURATION (À MODIFIER PAR VOS VALEURS) ---
# Le nom du fichier qui contient l'UI principale (votre point d'entrée)
MODULE_UI_NAME = "Script" 
# Le nom de la fonction qui ouvre votre fenêtre UI (si elle est définie, sinon la laisser comme dans l'exemple)
FUNCTION_UI_NAME = "Controller_Parameters_UI" 

# Liste de TOUTES les dépendances (pour le nettoyage du cache)
MODULES_DEPENDANTS = [
    'ControllerParameters', 
    'Deformers_Joint', 
    'Joint_Bend', 
    'Mirror', 
    'Skeleton',
    'UI_Skeleton'
]

# ÉTAPE CRUCIALE : Path Finding
# Replace the path by the path of the folder where all the.py are
CHEMIN_DU_PROJET = r"C:\Users\Arthur\Desktop\Travail\Scripts\Rig_Interface_Construction\Tools-Rig" 
# -----------------------------------

print("\n--- DÉMARRAGE DU LANCEMENT FORCE ---")

try:
    # 1. Résoudre le ModuleNotFoundError : Ajouter le chemin temporairement
    if CHEMIN_DU_PROJET not in sys.path:
        sys.path.append(CHEMIN_DU_PROJET)
        print(f"-> Chemin ajouté temporairement à sys.path: {CHEMIN_DU_PROJET}")

    # 2. Nettoyage du cache pour tous les modules
    MODULES_A_NETTOYER = [MODULE_UI_NAME] + MODULES_DEPENDANTS
    for module_name in MODULES_A_NETTOYER:
        if module_name in sys.modules:
            del sys.modules[module_name]
            print(f"-> Cache vidé pour : {module_name}")

    # Construction du chemin complet vers le fichier UI
    FICHIER_UI_PATH = os.path.join(CHEMIN_DU_PROJET, f"{MODULE_UI_NAME}.py")
    
    # 3. Charger et Exécuter le module UI principal
    
    # CHARGEMENT CORRIGÉ AVEC ENCODAGE UTF-8
    with open(FICHIER_UI_PATH, 'r', encoding='utf-8') as f:
        code_frais = f.read()
    
    # Exécuter le code. Ceci définit globalement la fonction UI.
    exec(code_frais) 

    # 4. Lancement de la fonction principale (si elle existe)
    # Ceci est la manière la plus sûre de l'appeler :
    if FUNCTION_UI_NAME in locals():
        globals()[FUNCTION_UI_NAME]()
        print(f"✅ Fenêtre '{FUNCTION_UI_NAME}' ouverte avec le code frais.")
    else:
        # Si le script se lance sans fonction d'enveloppe, cela ne posera pas problème.
        print("✅ Script exécuté directement. Vérifiez la fenêtre.")

except FileNotFoundError:
    cmds.error(f"Erreur: Le fichier UI principal '{FICHIER_UI_PATH}' est introuvable. Vérifiez le chemin 'CHEMIN_DU_PROJET'.")
except Exception as e:
    cmds.error(f"🔴 Erreur critique lors du lancement après encodage : {e}")