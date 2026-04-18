import tkinter as tk
from tkinter import ttk

#faudra rajouter les fenetres secondaires de merde la : 'tk.Toplevel'

class AppComArt() :

    def __init__(self, root):

        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("1200x800")
        
        # Création du gestionnaire d'onglets
        self.onglets = ttk.Notebook(self.root)
        self.onglets.pack(expand=True, fill="both")

        #Création des pages :
        self.page_clients = ttk.Frame(self.onglets)
        self.page_factures = ttk.Frame(self.onglets)

        # Ajout des pages dans les onglets avec un titre
        self.onglets.add(self.page_clients, text="Gestion des Clients")
        self.onglets.add(self.page_factures, text="Facturation")

        # Insertion widgets dans page_clients et page_factures
        ttk.Label(self.page_clients, text="Liste des clients...").pack()
        ttk.Label(self.page_factures, text="Liste des factures...").pack()
    


if __name__ == "__main__" :

    root = tk.Tk()

    app = AppComArt(root)

    root.mainloop()