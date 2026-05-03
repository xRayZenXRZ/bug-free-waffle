import tkinter as tk
from tkinter import ttk
from dao.DAODevis import DAODevis
import tkinter.messagebox


class GestionDevis(tk.Frame):
    def __init__(self, parent,devis):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.devis = devis

        # Header avec infos utilisateur
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)

        ttk.Label(
            header,
            text=f"Gestion des Devis - {devis['prenom']} {devis['nom']}",
            font=('Arial', 18, 'bold')
        ).pack()

        ttk.Label(
            header,
            text=f"Rôle : {devis['role']}",
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
            text="➕ Ajouter devis",
            command=self.ajouter_devis
        ).pack(pady=5, fill='x')

        ttk.Button(
            frame_gauche,
            text="👁️ Voir les devis",
            command=self.afficher_devis
        ).pack(pady=5, fill='x')

        ttk.Button(
            frame_gauche,
            text="🗑️ Supprimer devis",
            command=self.supprimer_devis
        ).pack(pady=5, fill='x')

        ttk.Button(
            frame_gauche,
            text="❌ Désactiver compte utilisateur",
            command=self.desactiver_utilisateur
        ).pack(pady=5, fill='x')

        ttk.Button(
            frame_gauche,
            text="✅ Activer compte utilisateur",
            command=self.activer_utilisateur
        ).pack(pady=5, fill='x')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)

        ttk.Label(
            frame_droite,
            text="Liste des devis :",
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        # Créer le Treeview (tableau)
        colonnes = ('Numero', 'Date emission', 'Date validite', 'Prestation', 'quantite prevue', 'Montant','Statut','id client', 'numero contrat')
        self.tree = ttk.Treeview(
            frame_droite, columns=colonnes, show='headings', height=15)

        # Définir les en-têtes
        self.tree.heading('Numero', text='Numero')
        self.tree.heading('Date emission', text='Date emission')
        self.tree.heading('Date validite', text='Date validite')
        self.tree.heading('Prestation', text='Prestation')
        self.tree.heading('quantite prevue', text='quantite prevue')
        self.tree.heading('Montant', text='Montant')
        self.tree.heading('Statut', text='Statut')
        self.tree.heading('id client', text='id client')
        self.tree.heading('numero contrat',text='numero contrat')

        # Largeur des colonnes
        self.tree.column('Numero', width=50, anchor='center')
        self.tree.column('Date emission', width=100, anchor='center')
        self.tree.column('Date validite', width=100, anchor='center')
        self.tree.column('Prestation', width=200, anchor='center')
        self.tree.column('quantite prevue', width=100, anchor='center')
        self.tree.column('Montant', width=80, anchor='center')
        self.tree.column('Statut', width=80, anchor='center')
        self.tree.column('id client',width=80,anchor='center')
        self.tree.column('numero contrat',width=80,anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame_droite, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Placer le Treeview et la scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind double-clic (optionnel)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.afficher_devis()

    def afficher_devis(self):
        """Affiche tous les utilisateurs dans le tableau"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Récupérer tous les utilisateurs via le DAO
        devis = DAODevis.get_all_devis

        # Insérer chaque utilisateur dans le tableau
        for devis in devis:
            self.tree.insert('', 'end', values=(
                devis['numeroDevis'],
                devis['dateEmission'],
                devis['dateValidite'],
                devis['descriptionPrestation'],
                devis['quantitePrevue'],
                devis['montantTotalEstime'],
                devis['statut'],
                devis['idClient'],
                devis['numeroContrat']
            ))

        print(f"{len(devis)} devis affiché(s)")

    def ajouter_devis(self):
        """Ouvre une fenêtre popup pour ajouter un devis"""

        # Créer une fenêtre popup
        popup = tk.Toplevel(self)
        popup.title("Ajouter un devis")
        popup.geometry("400x350")
        popup.resizable(False, False)

        # Centrer la fenêtre
        popup.transient(self)
        popup.grab_set()  # Rendre la fenêtre modale

        # Titre
        ttk.Label(
            popup,
            text="Créer un nouveau devis",
            font=('Arial', 14, 'bold')
        ).pack(pady=15)

        # Frame pour le formulaire
        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Champs du formulaire
        ttk.Label(form_frame, text="Numero :").grid(
            row=0, column=0, sticky='w', pady=5)
        entry_numero = ttk.Entry(form_frame, width=30)
        entry_numero.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date emission :").grid(
            row=1, column=0, sticky='w', pady=5)
        entry_date_emission = ttk.Entry(form_frame, width=30)
        entry_date_emission.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date validite :").grid(
            row=2, column=0, sticky='w', pady=5)
        entry_date_validite = ttk.Entry(form_frame, width=30)
        entry_date_validite.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Prestation :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_prestation = ttk.Entry(form_frame, width=30, show="*")
        entry_prestation.grid(row=3, column=1, pady=5, padx=5)
#        colonnes = ('Numero', 'Date emission', 'Date validite', 'Prestation', 'quantite prevue', 'Montant','Statut','id client', 'numero contrat')

        ttk.Label(form_frame, text="quantite prevue :").grid(
            row=4, column=0, sticky='w', pady=5)
        entry_quantiteprevue = ttk.Combobox(form_frame, width=28, state='readonly')
        entry_quantiteprevue.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Prestation :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_prestation = ttk.Entry(form_frame, width=30, show="*")
        entry_prestation.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Prestation :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_prestation = ttk.Entry(form_frame, width=30, show="*")
        entry_prestation.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Prestation :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_prestation = ttk.Entry(form_frame, width=30, show="*")
        entry_prestation.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Prestation :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_prestation = ttk.Entry(form_frame, width=30, show="*")
        entry_prestation.grid(row=3, column=1, pady=5, padx=5)
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
            succes, erreur = DAODevis.insert_devis(
                numeroDevis, dateEmission, dateValidite, descriptionPrestation, quantitePrevue, detailsCouts, montantTotalEstime, statut, dateAcceptation, idClient, numeroContrat  # ID de l'admin qui crée
            )

            if succes:
                tk.messagebox.showinfo(
                    "Succès", f"Utilisateur {prenom} {nom} créé avec succès !")
                popup.destroy()
                self.afficher_utilisateurs()  # Rafraîchir la liste
            else:
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

    def supprimer_devis(self):
        """Supprime l'utilisateur sélectionné"""

        # Récupérer l'élément sélectionné
        selection = self.tree.selection()

        if not selection:
            tk.messagebox.showwarning(
                "Aucune sélection", "Veuillez sélectionner un devis")
            return

        # Récupérer les valeurs de la ligne sélectionnée
        item = self.tree.item(selection[0])
        values = item['values']

        numero_devis = values[0]
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
