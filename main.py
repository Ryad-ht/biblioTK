import psycopg2
import json
import tkinter as tk
from tkinter import ttk

# conn = psycopg2.connect(
#     user="postgres",
#     password="root",
#     host="localhost",
#     port="5432",
#     database="alexandrie"
#     )
####### Code de remplisage exemple pour remplire la data de notes_livres.json sur notre base de donnesLivres_note ########
#  #Chargement des données depuis le fichier JSON
# with open('notes_livres.json') as json_file:
#     data = json.load(json_file)
#
# # Création d'un curseur pour exécuter les requêtes
# cur = conn.cursor()
#
# # Insérer les données dans la table
# for entry in data:
#     cur.execute("""
#         INSERT INTO Livre_note (livre_id, note_id,utilisateur_id)
#         VALUES (%s, %s, %s)""", (entry['livre_id'], entry['note_id'], entry['utilisateur_id']))
#
# # Valider les modifications et fermer la connexion
# conn.commit()
# cur.close()
# conn.close()


# Fonction pour afficher les données d'une table spécifique
def afficher_donnees(table_name, tab_frame):
    conn = psycopg2.connect(database="alexandrie", user="postgres", password="root",
                            host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()

    # Création du Treeview
    tree = ttk.Treeview(tab_frame)

    # Colonnes du Treeview avec les en-têtes
    column_names = [desc[0] for desc in cur.description]
    tree["columns"] = column_names
    tree.heading("#0", text="ID")  # Colonne ID (peut être modifiée en fonction de votre base de données)

    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    # Ajout des données dans le Treeview
    index = 1
    for row in rows:
        tree.insert("", index, text=index, values=row)
        index += 1

    tree.pack()

    cur.close()
    conn.close()


# Fonction pour créer l'interface avec les onglets
def creer_interface():
    fenetre = tk.Tk()
    fenetre.title("Affichage des tables")

    # Notebook (carnet d'onglets) pour contenir les onglets
    notebook = ttk.Notebook(fenetre)

    # Dictionnaire pour stocker les cadres (frames) pour chaque onglet
    tab_frames = {}

    # Liste des noms de tables
    tables = ['Auteurs', 'Utilisateurs', 'Livre', 'Reservation', 'Note', 'Livre_note']

    # Créer des onglets pour chaque table
    for table in tables:
        tab_frames[table] = ttk.Frame(notebook)
        notebook.add(tab_frames[table], text=table)
        # Appel de la fonction pour afficher les données dans chaque onglet
        afficher_donnees(table, tab_frames[table])

    # Ajouter le Notebook à la fenêtre principale
    notebook.pack(fill='both', expand=True)

    fenetre.mainloop()

# Appel de la fonction pour créer l'interface
creer_interface()
