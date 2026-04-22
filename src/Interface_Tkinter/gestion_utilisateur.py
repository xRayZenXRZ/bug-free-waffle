import tkinter as tk
from tkinter import ttk
from dao.DAOUtilisateur import DAOUtilisateur
import tkinter.messagebox


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
            text=f"Gestion des Utilisateurs - {utilisateur['prenom']} {utilisateur['nom']}",
            font=('Arial', 18, 'bold')
        ).pack()

        ttk.Label(
            header,
            text=f"Rôle : {utilisateur['role']}",
            font=('Arial', 12),
            foreground='blue'
        ).pack()

        # Frame principale avec 2 colonnes
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # COLONNE GAUCHE : Boutons
        frame_gauche = ttk.Frame(main_frame)
        frame_gauche.pack(side='left', fill='y', padx=10)

        ttk.Label(
            frame_gauche,
            text="Actions :",
            font=('Arial', 14, 'bold')
        ).pack(pady=10)

        ttk.Button(
            frame_gauche,
            text="➕ Ajouter utilisateur",
            command=self.ajouter_utilisateurs
        ).pack(pady=5, fill='x')

        ttk.Button(
            frame_gauche,
            text="👁️ Voir les utilisateurs",
            command=self.afficher_utilisateurs
        ).pack(pady=5, fill='x')

        ttk.Button(
            frame_gauche,
            text="🗑️ Supprimer utilisateur",
            command=self.supprimer_utilisateur
        ).pack(pady=5, fill='x')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)

        ttk.Label(
            frame_droite,
            text="Liste des utilisateurs :",
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        # Créer le Treeview (tableau)
        colonnes = ('ID', 'Nom', 'Prénom', 'Email', 'Rôle', 'Statut')
        self.tree = ttk.Treeview(
            frame_droite, columns=colonnes, show='headings', height=15)

        # Définir les en-têtes
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prénom', text='Prénom')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Rôle', text='Rôle')
        self.tree.heading('Statut', text='Statut')

        # Largeur des colonnes
        self.tree.column('ID', width=50)
        self.tree.column('Nom', width=100)
        self.tree.column('Prénom', width=100)
        self.tree.column('Email', width=200)
        self.tree.column('Rôle', width=100)
        self.tree.column('Statut', width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame_droite, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Placer le Treeview et la scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind double-clic (optionnel)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.afficher_utilisateurs()

    def afficher_utilisateurs(self):
        """Affiche tous les utilisateurs dans le tableau"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Récupérer tous les utilisateurs via le DAO
        utilisateurs = DAOUtilisateur.get_all_utilisateurs()

        # Insérer chaque utilisateur dans le tableau
        for user in utilisateurs:
            self.tree.insert('', 'end', values=(
                user['idUtilisateur'],
                user['nom'],
                user['prenom'],
                user['email'],
                user['role'],
                user['statut']
            ))

        print(f"{len(utilisateurs)} utilisateur(s) affiché(s)")

    def ajouter_utilisateurs(self):
        """Ouvre une fenêtre popup pour ajouter un utilisateur"""

        # Créer une fenêtre popup
        popup = tk.Toplevel(self)
        popup.title("Ajouter un utilisateur")
        popup.geometry("400x350")
        popup.resizable(False, False)

        # Centrer la fenêtre
        popup.transient(self)
        popup.grab_set()  # Rendre la fenêtre modale

        # Titre
        ttk.Label(
            popup,
            text="Créer un nouvel utilisateur",
            font=('Arial', 14, 'bold')
        ).pack(pady=15)

        # Frame pour le formulaire
        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Champs du formulaire
        ttk.Label(form_frame, text="Nom :").grid(
            row=0, column=0, sticky='w', pady=5)
        entry_nom = ttk.Entry(form_frame, width=30)
        entry_nom.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Prénom :").grid(
            row=1, column=0, sticky='w', pady=5)
        entry_prenom = ttk.Entry(form_frame, width=30)
        entry_prenom.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Email :").grid(
            row=2, column=0, sticky='w', pady=5)
        entry_email = ttk.Entry(form_frame, width=30)
        entry_email.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Mot de passe :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_mdp = ttk.Entry(form_frame, width=30, show="*")
        entry_mdp.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Rôle :").grid(
            row=4, column=0, sticky='w', pady=5)
        combo_role = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_role['values'] = ('ADMIN', 'COLLABORATEUR')
        combo_role.current(1)  # Par défaut COLLABORATEUR
        combo_role.grid(row=4, column=1, pady=5, padx=5)

        # Frame pour les boutons
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            """Valide et crée l'utilisateur"""
            nom = entry_nom.get().strip()
            prenom = entry_prenom.get().strip()
            email = entry_email.get().strip()
            mdp = entry_mdp.get()
            role = combo_role.get()

            # Validations
            if not nom or not prenom or not email or not mdp:
                tk.messagebox.showwarning(
                    "Champs manquants", "Veuillez remplir tous les champs")
                return

            if "@" not in email or "." not in email:
                tk.messagebox.showwarning(
                    "Email invalide", "Veuillez entrer un email valide")
                return

            # Créer l'utilisateur via le DAO
            succes, erreur = DAOUtilisateur.creer_utilisateur(
                nom, prenom, email, mdp, role,
                self.utilisateur['idUtilisateur']  # ID de l'admin qui crée
            )
            
            if succes:
                tk.messagebox.showinfo(
                    "Succès", f"Utilisateur {prenom} {nom} créé avec succès !")
                popup.destroy()
                self.afficher_utilisateurs()  # Rafraîchir la liste
            else :
                print(f"Erreur : {erreur}")

        def annuler():
            """Ferme la popup"""
            popup.destroy()

        # Boutons Valider et Annuler
        ttk.Button(btn_frame, text="✓ Valider",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler",
                   command=annuler).pack(side='left', padx=5)

        # Focus sur le premier champ
        entry_nom.focus()

    def supprimer_utilisateur(self):
        """Supprime l'utilisateur sélectionné"""

        # Récupérer l'élément sélectionné
        selection = self.tree.selection()

        if not selection:
            tk.messagebox.showwarning(
                "Aucune sélection", "Veuillez sélectionner un utilisateur")
            return

        # Récupérer les valeurs de la ligne sélectionnée
        item = self.tree.item(selection[0])
        values = item['values']

        id_utilisateur = values[0]
        nom = values[1]
        prenom = values[2]

        # Vérifier que l'utilisateur ne se supprime pas lui-même
        if id_utilisateur == self.utilisateur['idUtilisateur']:
            tk.messagebox.showerror(
                "Action interdite", "Vous ne pouvez pas supprimer votre propre compte !")
            return

        # Confirmation
        reponse = tk.messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer {prenom} {nom} ?"
        )

        if reponse:
            # Appeler le DAO pour supprimer
            succes = DAOUtilisateur.supprimer_utilisateur(id_utilisateur)

            if succes:
                # Supprimer visuellement de la liste
                self.tree.delete(selection[0])
                tk.messagebox.showinfo("Succès", "Utilisateur supprimé")
            else:
                tk.messagebox.showerror(
                    "Erreur", "Impossible de supprimer l'utilisateur")

    def on_double_click(self, event):
        """Appelé lors d'un double-clic sur une ligne"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            tk.messagebox.showinfo(
                "Détails",
                f"Utilisateur sélectionné : {item['values']}"
            )
