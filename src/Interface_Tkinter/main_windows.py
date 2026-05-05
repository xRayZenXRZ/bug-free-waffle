import tkinter as tk
from tkinter import ttk
import Interface_Tkinter.exportation 


<<<<<<< HEAD
class MainWindow(tk.Frame):
    def __init__(self, parent, utilisateur, on_gestion_users_callback, on_gestion_client_callback, on_gestion_devis_callback):
=======
class main_windows(tk.Frame):
    def __init__(self, parent, utilisateur, on_gestion_users_callback):

>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        self.utilisateur = utilisateur
        self.on_gestion_users = on_gestion_users_callback
<<<<<<< HEAD
        self.on_gestion_client = on_gestion_client_callback
        self.on_gestion_devis = on_gestion_devis_callback
=======
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357

        # Header avec infos utilisateur
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)
<<<<<<< HEAD
=======

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
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357

        ttk.Label(
<<<<<<< HEAD
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
=======
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
            content,
            text="Que souhaitez-vous faire ?",
            font=('Arial', 14)
        ).pack(pady=30)
<<<<<<< HEAD

        # Boutons selon le rôle
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(
                content,
                text="👥 Gérer les utilisateurs",
                command=lambda: self.on_gestion_users()
            ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="👤 Voir les clients",
            command=lambda: self.on_gestion_client()
        ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="📄 Gérer les devis",
            command=lambda: self.on_gestion_devis()
        ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="icon Gérer les prestation et activites",
            command=lambda: None
        ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="icon Exportation",
            command= Interface_Tkinter.exportation.exportation_combined_csv()
=======

        # Boutons selon le rôle
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(
                content,
                text="👥 Gérer les utilisateurs",
                command=lambda: self.on_gestion_users()
            ).pack(pady=10, ipadx=20, ipady=5)

        # Exemple de boutons
        ttk.Button(
            content,
            text="👤 Voir les clients",
            command=lambda: print("Voir clients")
        ).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(
            content,
            text="📄 Créer un devis",
            command=lambda: print("Créer devis")
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
        ).pack(pady=10, ipadx=20, ipady=5)
