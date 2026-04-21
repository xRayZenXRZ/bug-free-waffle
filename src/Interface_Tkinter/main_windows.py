import tkinter as tk
from tkinter import ttk


class main_windows(tk.Frame):
    def __init__(self, parent, nom_utilisateur):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Titre de bienvenue
        ttk.Label(
            self,
            text=f"Bienvenue {nom_utilisateur} !",
            font=('Arial', 24, 'bold')
        ).pack(pady=50)

        # Sous-titre
        ttk.Label(
            self,
            text="Que souhaitez-vous faire ?",
            font=('Arial', 14)
        ).pack(pady=20)

        # Exemple de boutons
        ttk.Button(
            self,
            text="Voir mes clients",
            command=lambda: print("Clic sur clients")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Créer une facture",
            command=lambda: print("Clic sur factures")
        ).pack(pady=10)
