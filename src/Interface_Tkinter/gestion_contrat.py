import tkinter as tk
from tkinter import ttk, messagebox
from dao.DAOContrat import DAOContrat
from dao.DAOClient import DAOClient
from dao.DAOPrestation import DAOPrestation
from dao.DAOActivite import DAOActivite
from dao.DAOCollaborateur import DAOCollaborateur
from domaine.Contrat import Contrat
from domaine.Prestation import Prestation
from domaine.Activite import Activite
from datetime import date
from tkcalendar import DateEntry


class GestionContrat(tk.Frame):
    def __init__(self, parent, utilisateur, on_back=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur

        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)
        ttk.Label(
            header,
            text=f"Gestion des Contrats - {utilisateur['prenom']} {utilisateur['nom']}",
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
        frame_gauche.pack(side='left', fill='both', padx=10)

        ttk.Label(frame_gauche, text="Actions :", font=('Arial', 14, 'bold')).pack(pady=10)
        ttk.Button(frame_gauche, text="➕ Créer un contrat",
                   command=self.ajouter_contrat).pack(pady=5, fill='x')
        ttk.Button(frame_gauche, text="👁️ Voir les contrats",
                   command=self.afficher_contrat).pack(pady=5, fill='x')
        ttk.Button(frame_gauche, text="🗓 Gérer prestations",
                   command=self._ouvrir_prestations_contrat_selectionne).pack(pady=5, fill='x')
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(frame_gauche, text="🗑️ Supprimer contrat",
                       command=self.supprimer_contrat).pack(pady=5, fill='x')
        if on_back:
            ttk.Label(frame_gauche, text="").pack(expand=True)
            ttk.Button(frame_gauche, text="🏠 Accueil", command=on_back).pack(
                pady=5, fill='x', side='bottom')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)
        ttk.Label(frame_droite, text="Liste des contrats :",
                  font=('Arial', 12, 'bold')).pack(pady=5)

        colonnes = ('Numéro', 'Date début', 'Durée',
                    'Nombre de prestations totales', 'Périodicité', 'Montant du contrat', 'Type de paiement', 'Client')
        self.tree = ttk.Treeview(
            frame_droite, columns=colonnes, show='headings', height=15)

        for col in colonnes:
            self.tree.heading(col, text=col)

        self.tree.column('Numéro',                        width=110, anchor='center')
        self.tree.column('Date début',                    width=100, anchor='center')
        self.tree.column('Durée',                         width=100, anchor='center')
        self.tree.column('Nombre de prestations totales', width=200, anchor='w')
        self.tree.column('Périodicité',                   width=80,  anchor='center')
        self.tree.column('Montant du contrat',            width=90,  anchor='center')
        self.tree.column('Type de paiement',              width=60,  anchor='center')
        self.tree.column('Client',                        width=110, anchor='center')

        scrollbar_x = ttk.Scrollbar(frame_droite, orient='horizontal', command=self.tree.xview)
        scrollbar_x.pack(side='bottom', fill='x')
        scrollbar = ttk.Scrollbar(frame_droite, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(fill='both', expand=True)

        self.tree.bind('<Double-1>', self.on_double_click)
        self.afficher_contrat()

    # ------------------------------------------------------------------ #

    def afficher_contrat(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        contrat_liste = DAOContrat.get_instance().select_contrat()

        for c in contrat_liste:
            self.tree.insert('', 'end', values=(
                c.get_numero_contrat(),
                c.get_date_debut(),
                c.get_duree(),
                c.get_nb_productions_totales(),
                c.get_periodicite(),
                f"{c.get_montant_global()} €",
                c.get_condition_paiements(),
                c.get_id_client(),
            ))
        print(f"{len(contrat_liste)} contrat(s) affiché(s)")

    # ------------------------------------------------------------------ #

    def ajouter_contrat(self):
        if hasattr(self, '_popup_ajout') and self._popup_ajout and self._popup_ajout.winfo_exists():
            self._popup_ajout.focus()
            return

        popup = tk.Toplevel(self)
        self._popup_ajout = popup
        popup.title("Créer un contrat")
        popup.geometry("500x490")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        # Génération automatique du numéro
        annee = date.today().year
        contrat_liste = DAOContrat.get_instance().select_contrat()
        numeros = [
            c.get_numero_contrat() for c in contrat_liste
            if c.get_numero_contrat() and str(annee) in c.get_numero_contrat()
        ]
        numero_seq = int(max(numeros).split('-')[-1]) + 1 if numeros else 1
        numero_auto = f"CONT-{annee}-{numero_seq:03d}"

        ttk.Label(popup, text="Créer un nouveau contrat", font=('Arial', 14, 'bold')).pack(pady=15)

        form = ttk.Frame(popup)
        form.pack(padx=20, pady=5, fill='both', expand=True)

        # Numéro (auto)
        ttk.Label(form, text="Numéro :").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Label(form, text=numero_auto, foreground='blue').grid(row=0, column=1, sticky='w', pady=5, padx=5)

        # Client
        ttk.Label(form, text="Client :").grid(row=1, column=0, sticky='w', pady=5)
        client_var = tk.StringVar(value="Aucun client sélectionné")
        ttk.Label(form, textvariable=client_var, foreground='blue').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        client_selectionne = {'id': None}

        def choisir_client():
            popup_client = tk.Toplevel(popup)
            popup_client.title("Choisir un client")
            popup_client.geometry("620x300")
            popup_client.transient(popup)
            popup_client.grab_set()

            ttk.Label(popup_client, text="Sélectionnez un client :",
                      font=('Arial', 12, 'bold')).pack(pady=10)

            cols = ('ID', 'Type', 'Nom', 'Prénom', 'Raison Sociale', 'Email', 'Statut')
            tree_c = ttk.Treeview(popup_client, columns=cols, show='headings', height=8)
            for col in cols:
                tree_c.heading(col, text=col)
            tree_c.column('ID',             width=40,  anchor='center')
            tree_c.column('Type',           width=90,  anchor='center')
            tree_c.column('Nom',            width=100, anchor='center')
            tree_c.column('Prénom',         width=100, anchor='center')
            tree_c.column('Raison Sociale', width=130, anchor='center')
            tree_c.column('Email',          width=150, anchor='center')
            tree_c.column('Statut',         width=80,  anchor='center')
            tree_c.pack(fill='both', expand=True, padx=10)

            for c in DAOClient.get_instance().select_client():
                tree_c.insert('', 'end', values=(
                    c.get_id_client(),
                    'ENTREPRISE' if c.get_raison_sociale() else 'PARTICULIER',
                    c.get_nom() or '',
                    c.get_prenom() or '',
                    c.get_raison_sociale() or '',
                    c.get_courriel(),
                    c.get_status_client()
                ))

            def confirmer_client():
                sel = tree_c.selection()
                if not sel:
                    messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client")
                    return
                valeurs = tree_c.item(sel[0])['values']
                client_selectionne['id'] = valeurs[0]
                nom_affiche = valeurs[2] or valeurs[4]
                client_var.set(f"{valeurs[0]} - {nom_affiche}")
                popup_client.destroy()

            ttk.Button(popup_client, text="✓ Choisir", command=confirmer_client).pack(pady=10)

        ttk.Button(form, text="👤 Choisir", command=choisir_client).grid(row=1, column=2, padx=5)

        # Date début
        ttk.Label(form, text="Date début :").grid(row=2, column=0, sticky='w', pady=5)
        entry_debut = DateEntry(form, width=28, date_pattern='yyyy-mm-dd')
        entry_debut.grid(row=2, column=1, pady=5, padx=5)

        # Durée
        ttk.Label(form, text="Durée :").grid(row=3, column=0, sticky='w', pady=5)
        entry_duree = ttk.Entry(form, width=30)
        entry_duree.grid(row=3, column=1, pady=5, padx=5)

        # Nb productions
        ttk.Label(form, text="Nb productions :").grid(row=4, column=0, sticky='w', pady=5)
        entry_nb = ttk.Entry(form, width=30)
        entry_nb.grid(row=4, column=1, pady=5, padx=5)

        # Périodicité
        ttk.Label(form, text="Périodicité :").grid(row=5, column=0, sticky='w', pady=5)
        combo_periode = ttk.Combobox(form, width=28, state='readonly')
        combo_periode['values'] = ('HEBDOMADAIRE', 'MENSUELLE', 'ANNUELLE')
        combo_periode.current(1)
        combo_periode.grid(row=5, column=1, pady=5, padx=5)

        # Montant
        ttk.Label(form, text="Montant global (€) :").grid(row=6, column=0, sticky='w', pady=5)
        entry_montant = ttk.Entry(form, width=30)
        entry_montant.grid(row=6, column=1, pady=5, padx=5)

        # Conditions paiement
        ttk.Label(form, text="Conditions paiement :").grid(row=7, column=0, sticky='w', pady=5)
        entry_conditions = ttk.Entry(form, width=30)
        entry_conditions.grid(row=7, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            if not client_selectionne['id']:
                messagebox.showwarning("Client manquant", "Veuillez sélectionner un client")
                return

            duree = entry_duree.get().strip()
            nb = entry_nb.get().strip()
            montant = entry_montant.get().strip()
            conditions = entry_conditions.get().strip()
            debut = str(entry_debut.get_date())

            if not duree or not nb or not montant or not conditions:
                messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return

            try:
                nb_i = int(nb)
                montant_f = float(montant)
                id_client_i = int(client_selectionne['id'])
            except ValueError:
                messagebox.showwarning("Valeur invalide", "Nb productions et montant doivent être numériques")
                return

            nouveau = Contrat(numero_auto, debut, duree, nb_i,
                              combo_periode.get(), montant_f, conditions, id_client_i)
            cle = DAOContrat.get_instance().insert_contrat(nouveau)

            if cle != -1:
                messagebox.showinfo("Succès", f"Contrat {numero_auto} créé !\n\nVous pouvez maintenant ajouter des prestations.")
                self.afficher_contrat()
                popup.destroy()
                self._ouvrir_gestion_prestations(numero_auto)
            else:
                messagebox.showerror("Erreur", "Impossible de créer le contrat")

        ttk.Button(btn_frame, text="✓ Valider et ajouter des prestations",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler",
                   command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def _ouvrir_prestations_contrat_selectionne(self):
        """Ouvre la gestion des prestations pour le contrat sélectionné dans le tableau."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un contrat dans la liste")
            return
        numero_contrat = self.tree.item(selection[0])['values'][0]
        self._ouvrir_gestion_prestations(numero_contrat)

    def _ouvrir_gestion_prestations(self, numero_contrat):
        """Fenêtre de gestion des prestations d'un contrat."""
        popup = tk.Toplevel(self)
        popup.title(f"Prestations — contrat {numero_contrat}")
        popup.geometry("760x500")
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Prestations du contrat {numero_contrat}",
                  font=('Arial', 13, 'bold')).pack(pady=10)

        cols = ('ID', 'Date prévue', 'Lieu', 'Type', 'Nb photos', 'Nb vidéos')
        frame_tree = ttk.Frame(popup)
        frame_tree.pack(fill='both', expand=True, padx=15)

        tree = ttk.Treeview(frame_tree, columns=cols, show='headings', height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=115)
        sb = ttk.Scrollbar(frame_tree, orient='vertical', command=tree.yview)
        sb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=sb.set)
        tree.pack(fill='both', expand=True)

        def rafraichir_prestations():
            tree.delete(*tree.get_children())
            critere = Prestation(-1, numero_contrat=numero_contrat)
            for p in DAOPrestation.get_instance().select_prestation(critere):
                tree.insert('', 'end', values=(
                    p.get_id_prestation(),
                    p.get_date_prevue() or '',
                    p.get_lieu() or '',
                    p.get_type() or '',
                    p.get_nb_photos_prevues() or 0,
                    p.get_nb_videos_prevues() or 0,
                ))

        rafraichir_prestations()

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=10)

        def gerer_activites():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une prestation")
                return
            id_prestation = tree.item(sel[0])['values'][0]
            self._popup_gerer_activites(id_prestation, popup)

        ttk.Button(btn_frame, text="➕ Ajouter une prestation",
                   command=lambda: self._popup_ajouter_prestation(numero_contrat, rafraichir_prestations, popup)
                   ).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗓 Gérer les activités",
                   command=gerer_activites).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✓ Terminer",
                   command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def _popup_ajouter_prestation(self, numero_contrat, rafraichir, parent):
        """Formulaire d'ajout d'une prestation à un contrat."""
        popup = tk.Toplevel(parent)
        popup.title("Ajouter une prestation")
        popup.geometry("420x340")
        popup.resizable(False, False)
        popup.transient(parent)
        popup.grab_set()

        ttk.Label(popup, text="Nouvelle prestation", font=('Arial', 13, 'bold')).pack(pady=12)

        form = ttk.Frame(popup)
        form.pack(padx=20, pady=5, fill='both', expand=True)

        ttk.Label(form, text="Date prévue :").grid(row=0, column=0, sticky='w', pady=5)
        entry_date = DateEntry(form, width=28, date_pattern='yyyy-mm-dd')
        entry_date.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form, text="Lieu :").grid(row=1, column=0, sticky='w', pady=5)
        entry_lieu = ttk.Entry(form, width=30)
        entry_lieu.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form, text="Type :").grid(row=2, column=0, sticky='w', pady=5)
        combo_type = ttk.Combobox(form, width=28, state='readonly')
        combo_type['values'] = ('PHOTO', 'VIDEO', 'MIXTE')
        combo_type.current(0)
        combo_type.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form, text="Nb photos prévues :").grid(row=3, column=0, sticky='w', pady=5)
        entry_photos = ttk.Entry(form, width=30)
        entry_photos.insert(0, "0")
        entry_photos.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form, text="Nb vidéos prévues :").grid(row=4, column=0, sticky='w', pady=5)
        entry_videos = ttk.Entry(form, width=30)
        entry_videos.insert(0, "0")
        entry_videos.grid(row=4, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            date_prevue = str(entry_date.get_date())
            lieu = entry_lieu.get().strip() or None
            type_p = combo_type.get()

            try:
                nb_photos = int(entry_photos.get().strip())
                nb_videos = int(entry_videos.get().strip())
            except ValueError:
                messagebox.showwarning("Valeur invalide", "Nb photos et vidéos doivent être des entiers")
                return

            nouvelle = Prestation(
                None,
                date_prevue=date_prevue,
                date_effective=None,
                lieu=lieu,
                type_prestation=type_p,
                nb_photos_prevues=nb_photos,
                nb_videos_prevues=nb_videos,
                numero_contrat=numero_contrat
            )

            if nouvelle.get_id_prestation() and nouvelle.get_id_prestation() != -1:
                messagebox.showinfo("Succès", "Prestation ajoutée !")
                rafraichir()
                popup.destroy()
            else:
                messagebox.showerror("Erreur", "Impossible d'ajouter la prestation")

        ttk.Button(btn_frame, text="✓ Valider", command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler", command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def _popup_gerer_activites(self, id_prestation, parent):
        """Fenêtre de gestion des activités d'une prestation."""
        popup = tk.Toplevel(parent)
        popup.title(f"Activités — prestation #{id_prestation}")
        popup.geometry("760x440")
        popup.transient(parent)
        popup.grab_set()

        ttk.Label(popup, text=f"Activités de la prestation #{id_prestation}",
                  font=('Arial', 13, 'bold')).pack(pady=10)

        cols = ('ID', 'Libellé', 'Date prévue', 'Durée (h)', 'Collaborateur', 'Statut')
        frame_tree = ttk.Frame(popup)
        frame_tree.pack(fill='both', expand=True, padx=15)

        tree = ttk.Treeview(frame_tree, columns=cols, show='headings', height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=115)
        sb = ttk.Scrollbar(frame_tree, orient='vertical', command=tree.yview)
        sb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=sb.set)
        tree.pack(fill='both', expand=True)

        def rafraichir_activites():
            tree.delete(*tree.get_children())
            critere = Activite(-1, id_prestation=id_prestation)
            for a in DAOActivite.get_instance().select_activite(critere):
                tree.insert('', 'end', values=(
                    a.get_id_activite(),
                    a.get_libelle_operationnel() or '',
                    a.get_date_prevues() or '',
                    a.get_duree_estimee() or 0,
                    a.get_id_collaborateur() or '',
                    a.get_statut() or '',
                ))

        rafraichir_activites()

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ Ajouter une activité",
                   command=lambda: self._popup_ajouter_activite(id_prestation, rafraichir_activites, popup)
                   ).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✓ Terminer",
                   command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def _popup_ajouter_activite(self, id_prestation, rafraichir, parent):
        """Formulaire d'ajout d'une activité à une prestation."""
        popup = tk.Toplevel(parent)
        popup.title("Ajouter une activité")
        popup.geometry("460x370")
        popup.resizable(False, False)
        popup.transient(parent)
        popup.grab_set()

        ttk.Label(popup, text="Nouvelle activité", font=('Arial', 13, 'bold')).pack(pady=12)

        form = ttk.Frame(popup)
        form.pack(padx=20, pady=5, fill='both', expand=True)

        ttk.Label(form, text="Libellé :").grid(row=0, column=0, sticky='w', pady=5)
        entry_libelle = ttk.Entry(form, width=30)
        entry_libelle.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form, text="Date prévue :").grid(row=1, column=0, sticky='w', pady=5)
        entry_date = DateEntry(form, width=28, date_pattern='yyyy-mm-dd')
        entry_date.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form, text="Durée estimée (h) :").grid(row=2, column=0, sticky='w', pady=5)
        entry_duree = ttk.Entry(form, width=30)
        entry_duree.insert(0, "1")
        entry_duree.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form, text="Collaborateur :").grid(row=3, column=0, sticky='w', pady=5)
        collab_var = tk.StringVar(value="Aucun sélectionné")
        ttk.Label(form, textvariable=collab_var, foreground='blue').grid(row=3, column=1, sticky='w', pady=5, padx=5)
        collab_selectionne = {'id': None}

        def choisir_collaborateur():
            popup_c = tk.Toplevel(popup)
            popup_c.title("Choisir un collaborateur")
            popup_c.geometry("500x280")
            popup_c.transient(popup)
            popup_c.grab_set()

            ttk.Label(popup_c, text="Sélectionnez un collaborateur :",
                      font=('Arial', 12, 'bold')).pack(pady=10)

            cols_c = ('ID', 'Nom', 'Prénom', 'Poste')
            tree_c = ttk.Treeview(popup_c, columns=cols_c, show='headings', height=8)
            for col in cols_c:
                tree_c.heading(col, text=col)
                tree_c.column(col, anchor='center', width=110)
            tree_c.pack(fill='both', expand=True, padx=10)

            for c in DAOCollaborateur.get_instance().select_collaborateur():
                tree_c.insert('', 'end', values=(
                    c.get_id_collaborateur(),
                    c.get_nom(),
                    c.get_prenom(),
                    c.get_poste() or ''
                ))

            def confirmer_collab():
                sel = tree_c.selection()
                if not sel:
                    messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un collaborateur")
                    return
                valeurs = tree_c.item(sel[0])['values']
                collab_selectionne['id'] = valeurs[0]
                collab_var.set(f"{valeurs[0]} - {valeurs[1]} {valeurs[2]}")
                popup_c.destroy()

            ttk.Button(popup_c, text="✓ Choisir", command=confirmer_collab).pack(pady=10)

        ttk.Button(form, text="👤 Choisir", command=choisir_collaborateur).grid(row=3, column=2, padx=5)

        ttk.Label(form, text="Statut :").grid(row=4, column=0, sticky='w', pady=5)
        combo_statut = ttk.Combobox(form, width=28, state='readonly')
        combo_statut['values'] = ('PLANIFIE', 'EN_COURS', 'TERMINE', 'ANNULE')
        combo_statut.current(0)
        combo_statut.grid(row=4, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            libelle = entry_libelle.get().strip()
            if not libelle:
                messagebox.showwarning("Champ manquant", "Veuillez saisir un libellé")
                return

            try:
                duree = int(entry_duree.get().strip())
            except ValueError:
                messagebox.showwarning("Valeur invalide", "La durée doit être un entier")
                return

            date_prevue = str(entry_date.get_date())
            statut = combo_statut.get()

            nouvelle = Activite(
                None,
                libelle_operationnel=libelle,
                date_prevues=date_prevue,
                date_effective=None,
                duree_estimee=duree,
                id_collaborateur=collab_selectionne['id'],
                statut=statut,
                id_prestation=id_prestation
            )

            if nouvelle.get_id_activite() and nouvelle.get_id_activite() != -1:
                messagebox.showinfo("Succès", "Activité ajoutée !")
                rafraichir()
                popup.destroy()
            else:
                messagebox.showerror("Erreur", "Impossible d'ajouter l'activité")

        ttk.Button(btn_frame, text="✓ Valider", command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler", command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def supprimer_contrat(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un contrat")
            return

        values = self.tree.item(selection[0])['values']
        numero = values[0]

        reponse = messagebox.askyesno(
            "Confirmation", f"Voulez-vous vraiment supprimer le contrat « {numero} » ?")

        if reponse:
            c = Contrat(numero, None, None, None, None, None, None, None)
            succes = DAOContrat.get_instance().delete_contrat(c)
            if succes:
                self.tree.delete(selection[0])
                messagebox.showinfo("Succès", "Contrat supprimé")
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer le contrat")

    # ------------------------------------------------------------------ #

    def on_double_click(self, _event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            messagebox.showinfo("Détails contrat", (
                f"Numéro              : {values[0]}\n"
                f"Date début          : {values[1]}\n"
                f"Durée               : {values[2]}\n"
                f"Nb productions tot. : {values[3]}\n"
                f"Périodicité         : {values[4]}\n"
                f"Montant du contrat  : {values[5]}\n"
                f"Type de paiement    : {values[6]}\n"
                f"Client ID           : {values[7]}"
            ))
