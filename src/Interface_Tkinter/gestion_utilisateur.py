import tkinter as tk
from tkinter import ttk


class GestionUtilisateur(tk.Frame):
    def __init__(self, parent, utilisateur):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.utilisateur = utilisateur

        # Header avec infos utilisateur
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)

        ttk.Label(
            header,
            text=f"Bienvenue {utilisateur['prenom']} {utilisateur['nom']} !",
            font=('Arial', 20, 'bold')
        ).pack()

        ttk.Label(
            header,
            text=f"Rôle : {utilisateur['role']}",
            font=('Arial', 12),
            foreground='blue'
        ).pack()

        # Zone de contenu
        content = ttk.Frame(self)
        content.pack(fill='both', expand=True, padx=50, pady=20)

        ttk.Label(
            content,
            text="Que souhaitez-vous faire ?",
            font=('Arial', 14)
        ).pack(pady=30)

        # Boutons selon le rôle
        ttk.Button(
            content,
            text="Ajouter utilisateurs",
            command=lambda: print("Ajouter utilisateurs")
        ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="👤 Voir les utilisateurs",
            command=lambda: print("Voir clients")
        ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="supprimer un utilisateur",
            command=lambda: print("supprimer un utilisateur")
        ).pack(pady=10, ipadx=20, ipady=5)