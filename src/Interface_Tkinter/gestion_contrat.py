import tkinter as tk
from tkinter import ttk
from dao.DAOContrat import DAOContrat
from dao.DAOClient import DAOClient
from domaine.Contrat import Contrat
from datetime import date
from tkcalendar import DateEntry
from dao.DAODevis import DAODevis


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

        ttk.Label(frame_gauche, text="Actions :", font=(
            'Arial', 14, 'bold')).pack(pady=10)
        '''ttk.Button(frame_gauche, text="➕ Créer un contrat",
                   command=self.ajouter_contrat).pack(pady=5, fill='x')'''
        ttk.Button(frame_gauche, text="👁️ Voir les contrats",
                   command=self.afficher_contrat).pack(pady=5, fill='x')
        '''ttk.Button(frame_gauche, text="✏️ Modifier statut",
                   command=self.modifier_contrat).pack(pady=5, fill='x')'''
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

        self.tree.column('Numéro',        width=110, anchor='center')
        self.tree.column('Date début', width=100, anchor='center')
        self.tree.column('Durée', width=100, anchor='center')
        self.tree.column('Nombre de prestations totales',   width=200, anchor='w')
        self.tree.column('Périodicité',       width=80,  anchor='center')
        self.tree.column('Montant du contrat',        width=90,  anchor='center')
        self.tree.column('Type de paiement',        width=60,  anchor='center')
        self.tree.column('Client',       width=110, anchor='center')

        scrollbar_x = ttk.Scrollbar(
            frame_droite, orient='horizontal', command=self.tree.xview)
        scrollbar_x.pack(side='bottom', fill='x')
        scrollbar = ttk.Scrollbar(
            frame_droite, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set,
                            xscrollcommand=scrollbar_x.set)
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
    
    def supprimer_contrat(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning(
                "Aucune sélection", "Veuillez sélectionner un contrat")
            return

        values = self.tree.item(selection[0])['values']
        numero = values[0]

        reponse = tk.messagebox.askyesno(
            "Confirmation", f"Voulez-vous vraiment supprimer le contrat « {numero} » ?")

        if reponse:
            c = Contrat(numero, None, None, None, None,
                      None, None, None)
            succes = DAOContrat.get_instance().delete_contrat(c)
            if succes:
                self.tree.delete(selection[0])
                tk.messagebox.showinfo("Succès", "Contrat supprimé")
            else:
                tk.messagebox.showerror(
                    "Erreur", "Impossible de supprimer le contrat")


    # ------------------------------------------------------------------ #


    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            tk.messagebox.showinfo("Détails contrat", (
                f"Numéro    : {values[0]}\n"
                f"Date début    : {values[1]}\n"
                f"Durée    : {values[2]}\n"
                f"Nombre de prestations totales    : {values[3]}\n"
                f"Périodicité    : {values[4]}\n"
                f"Montant du contrat    : {values[5]}\n"
                f"Type de paiement    : {values[6]}\n"
                f"Client ID    : {values[7]}"
            ))
    '''def ajouter_contrat(self):
        if hasattr(self, '_popup_ajout') and self._popup_ajout and self._popup_ajout.winfo_exists():
            self._popup_ajout.focus()
            return

        popup = tk.Toplevel(self)
        self._popup_ajout = popup
        popup.title("Créer un contrat")
        popup.geometry("480x500")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        def generer_numero():
            annee = date.today().year
            contrat_liste = DAOContrat.get_instance().select_contrat()
            numeros = [
                c.get_numero_contrat() for c in contrat_liste
                if c.get_numero_contrat() and str(annee) in c.get_numero_contrat()
            ]
            if numeros:
                dernier = max(numeros)
                numero_seq = int(dernier.split('-')[-1]) + 1
            else:
                numero_seq = 1
            return f"CONT-{annee}-{numero_seq:03d}"

        numero_auto = generer_numero()

        ttk.Label(popup, text="Créer un nouveau contrat",
                  font=('Arial', 14, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        ttk.Label(form_frame, text="Numéro contrat :").grid(
            row=0, column=0, sticky='w', pady=5)
        ttk.Label(form_frame, text=numero_auto, foreground='blue').grid(
            row=0, column=1, sticky='w', pady=5, padx=5)

        ttk.Label(form_frame, text="Contrat :").grid(
            row=1, column=0, sticky='w', pady=5)
        contrat_var = tk.StringVar(value="Aucun contrat sélectionné")
        ttk.Label(form_frame, textvariable=contrat_var, foreground='blue').grid(
            row=1, column=1, sticky='w', pady=5, padx=5)
        con_selectionne = {'id': None}

        def choisir_devis():
            popup_devis = tk.Toplevel(popup)
            popup_devis.title("Choisir un devis")
            popup_devis.geometry("600x300")
            popup_devis.transient(popup)
            popup_devis.grab_set()

            ttk.Label(popup_devis, text="Sélectionnez un client :",
                      font=('Arial', 12, 'bold')).pack(pady=10)

            cols = ('ID', 'Type', 'Nom', 'Prénom',
                    'Raison Sociale', 'Email', 'Statut')
            tree_devis = ttk.Treeview(
                popup_devis, columns=cols, show='headings', height=8)
            for col in cols:
                tree_devis.heading(col, text=col)
            tree_devis.column('ID',            width=40,  anchor='center')
            tree_devis.column('Type',          width=90,  anchor='center')
            tree_devis.column('Nom',           width=100, anchor='center')
            tree_devis.column('Prénom',        width=100, anchor='center')
            tree_devis.column('Raison Sociale', width=130, anchor='center')
            tree_devis.column('Email',         width=150, anchor='center')
            tree_devis.column('Statut',        width=80,  anchor='center')
            tree_devis.pack(fill='both', expand=True, padx=10)

            devis = DAODevis.get_instance().select_devis()
            for d in devis:
                tree_devis.insert('', 'end', values=(
                    d.get_numero_devis(),
                    'ENTREPRISE' if c.get_raison_sociale() else 'PARTICULIER',
                    c.get_nom() or '',
                    c.get_prenom() or '',
                    c.get_raison_sociale() or '',
                    c.get_courriel(),
                    c.get_status_client()
                ))

            def confirmer():
                sel = tree_client.selection()
                if not sel:
                    tk.messagebox.showwarning(
                        "Aucune sélection", "Veuillez sélectionner un client")
                    return
                valeurs = tree_client.item(sel[0])['values']
                client_selectionne['id'] = valeurs[0]
                nom_affiche = valeurs[2] or valeurs[4]
                client_var.set(f"{valeurs[0]} - {nom_affiche}")
                popup_client.destroy()

            ttk.Button(popup_client, text="✓ Choisir",
                       command=confirmer).pack(pady=10)

        ttk.Button(form_frame, text="👤 Choisir un client",
                   command=choisir_client).grid(row=1, column=2, padx=5)

        ttk.Label(form_frame, text="Description :").grid(
            row=2, column=0, sticky='w', pady=5)
        entry_desc = ttk.Entry(form_frame, width=30)
        entry_desc.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Quantité :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_qte = ttk.Entry(form_frame, width=30)
        entry_qte.insert(0, "1")
        entry_qte.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Détails coûts :").grid(
            row=4, column=0, sticky='w', pady=5)
        entry_couts = ttk.Entry(form_frame, width=30)
        entry_couts.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Montant (€) :").grid(
            row=5, column=0, sticky='w', pady=5)
        entry_montant = ttk.Entry(form_frame, width=30)
        entry_montant.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date émission :").grid(
            row=6, column=0, sticky='w', pady=5)
        entry_emission = DateEntry(
            form_frame, width=28, date_pattern='yyyy-mm-dd')
        entry_emission.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date validité :").grid(
            row=7, column=0, sticky='w', pady=5)
        entry_validite = DateEntry(
            form_frame, width=28, date_pattern='yyyy-mm-dd')
        entry_validite.grid(row=7, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            numero = numero_auto
            if not client_selectionne['id']:
                tk.messagebox.showwarning(
                    "Client manquant", "Veuillez sélectionner un client")
                return
            id_client = client_selectionne['id']
            desc = entry_desc.get().strip()
            qte = entry_qte.get().strip()
            couts = entry_couts.get().strip()
            montant = entry_montant.get().strip()
            emission = entry_emission.get_date()
            validite = entry_validite.get_date()

            if emission < date.today():
                tk.messagebox.showwarning(
                    "Date invalide", "La date d'émission ne peut pas être dans le passé")
                return
            if validite <= emission:
                tk.messagebox.showwarning(
                    "Date invalide", "La date de validité doit être après la date d'émission")
                return

            try:
                montant_f = float(montant)
                qte_i = int(qte)
                id_client_i = int(id_client)
            except ValueError:
                tk.messagebox.showwarning(
                    "Valeur invalide", "Montant, quantité et ID client doivent être numériques")
                return

            nouveau = Devis(numero, str(emission), str(
                validite), desc, qte_i, couts, montant_f, 'EN_ATTENTE', None, id_client_i, None)
            cle = DAODevis.get_instance().insert_devis(nouveau)

            if cle != -1:
                tk.messagebox.showinfo("Succès", "Devis créé avec succès !")
                popup.destroy()
                self.afficher_devis()
            else:
                tk.messagebox.showerror(
                    "Erreur", "Impossible de créer le devis")

        ttk.Button(btn_frame, text="✓ Valider",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler",
                   command=popup.destroy).pack(side='left', padx=5)'''

    # ------------------------------------------------------------------ #
#numeroContrat, dateDebut, duree, nbProductionsTotales, periodicite, montantGlobal, conditionsPaiement, idClient

'''    def modifier_(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning(
                "Aucune sélection", "Veuillez sélectionner un devis")
            return

        values = self.tree.item(selection[0])['values']

        popup = tk.Toplevel(self)
        popup.title("Modifier le statut")
        popup.geometry("320x180")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Devis : {values[0]}", font=(
            'Arial', 12, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10)

        ttk.Label(form_frame, text="Statut :").grid(
            row=0, column=0, sticky='w', pady=5)
        combo_statut = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_statut['values'] = ('EN_ATTENTE', 'ACCEPTE', 'REFUSE', 'EXPIRE')
        combo_statut.set(values[5])
        combo_statut.grid(row=0, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def _sauvegarder(numero_contrat, date_acceptation, nouveau_statut):
            modifie = Devis(
                values[0],
                str(values[1]),
                str(values[2]),
                str(values[3]),
                1,
                "",
                float(str(values[4]).replace(' €', '')),
                nouveau_statut,
                date_acceptation,
                int(values[6]),
                numero_contrat
            )
            succes = DAODevis.get_instance().update_devis(modifie)
            if succes:
                tk.messagebox.showinfo(
                    "Succès", f"Statut du devis {values[0]} mis à jour !")
                popup.destroy()
                self.afficher_devis()
            else:
                tk.messagebox.showerror(
                    "Erreur", "Impossible de modifier le statut")

        def _choisir_et_lier_contrat(date_acceptation):
            popup_contrat = tk.Toplevel(popup)
            popup_contrat.title("Choisir un contrat")
            popup_contrat.geometry("600x370")
            popup_contrat.transient(popup)
            popup_contrat.grab_set()

            popup_contrat.protocol("WM_DELETE_WINDOW", lambda: tk.messagebox.showwarning(
                "Obligatoire", "Vous devez sélectionner ou créer un contrat pour accepter ce devis."
            ))

            ttk.Label(popup_contrat, text="Sélectionnez un contrat :",
                      font=('Arial', 12, 'bold')).pack(pady=10)

            cols = ('Numéro', 'Date début', 'Durée',
                    'Périodicité', 'Montant', 'Client')
            tree_contrat = ttk.Treeview(
                popup_contrat, columns=cols, show='headings', height=8)
            for col in cols:
                tree_contrat.heading(col, text=col)
            tree_contrat.column('Numéro',      width=110, anchor='center')
            tree_contrat.column('Date début',  width=90,  anchor='center')
            tree_contrat.column('Durée',       width=70,  anchor='center')
            tree_contrat.column('Périodicité', width=90,  anchor='center')
            tree_contrat.column('Montant',     width=80,  anchor='center')
            tree_contrat.column('Client',      width=60,  anchor='center')
            tree_contrat.pack(fill='both', expand=True, padx=10)

            def charger_contrats():
                tree_contrat.delete(*tree_contrat.get_children())
                contrats = DAOContrat.get_instance().select_contrat()
                for c in contrats:
                    tree_contrat.insert('', 'end', values=(
                        c.get_numero_contrat(),
                        c.get_date_debut(),
                        c.get_duree(),
                        c.get_periodicite(),
                        f"{c.get_montant_global()} €",
                        c.get_id_client()
                    ))

            charger_contrats()

            def creer_contrat():
                popup_creer = tk.Toplevel(popup_contrat)
                popup_creer.title("Créer un contrat")
                popup_creer.geometry("480x420")
                popup_creer.resizable(False, False)
                popup_creer.transient(popup_contrat)
                popup_creer.grab_set()

                ttk.Label(popup_creer, text="Nouveau contrat",
                          font=('Arial', 14, 'bold')).pack(pady=15)

                form = ttk.Frame(popup_creer)
                form.pack(padx=20, pady=10, fill='both', expand=True)

                annee = date.today().year
                contrats = DAOContrat.get_instance().select_contrat()
                numeros = [c.get_numero_contrat() for c in contrats if str(
                    annee) in c.get_numero_contrat()]
                numero_seq = int(max(numeros).split(
                    '-')[-1]) + 1 if numeros else 1
                numero_contrat_auto = f"CONT-{annee}-{numero_seq:03d}"

                ttk.Label(form, text="Numéro :").grid(
                    row=0, column=0, sticky='w', pady=5)
                ttk.Label(form, text=numero_contrat_auto, foreground='blue').grid(
                    row=0, column=1, sticky='w', pady=5, padx=5)

                # Client — sélection via popup
                ttk.Label(form, text="Client :").grid(
                    row=1, column=0, sticky='w', pady=5)
                client_var_contrat = tk.StringVar(
                    value="Aucun client sélectionné")
                ttk.Label(form, textvariable=client_var_contrat, foreground='blue').grid(
                    row=1, column=1, sticky='w', pady=5, padx=5)
                client_selectionne_contrat = {'id': None}

                def choisir_client_contrat():
                    popup_client = tk.Toplevel(popup_creer)
                    popup_client.title("Choisir un client")
                    popup_client.geometry("600x300")
                    popup_client.transient(popup_creer)
                    popup_client.grab_set()

                    ttk.Label(popup_client, text="Sélectionnez un client :", font=(
                        'Arial', 12, 'bold')).pack(pady=10)

                    cols = ('ID', 'Type', 'Nom', 'Prénom',
                            'Raison Sociale', 'Email', 'Statut')
                    tree_client = ttk.Treeview(
                        popup_client, columns=cols, show='headings', height=8)
                    for col in cols:
                        tree_client.heading(col, text=col)
                    tree_client.column(
                        'ID',             width=40,  anchor='center')
                    tree_client.column(
                        'Type',           width=90,  anchor='center')
                    tree_client.column(
                        'Nom',            width=100, anchor='center')
                    tree_client.column(
                        'Prénom',         width=100, anchor='center')
                    tree_client.column(
                        'Raison Sociale', width=130, anchor='center')
                    tree_client.column(
                        'Email',          width=150, anchor='center')
                    tree_client.column(
                        'Statut',         width=80,  anchor='center')
                    tree_client.pack(fill='both', expand=True, padx=10)

                    clients = DAOClient.get_instance().select_client()
                    for c in clients:
                        tree_client.insert('', 'end', values=(
                            c.get_id_client(),
                            'ENTREPRISE' if c.get_raison_sociale() else 'PARTICULIER',
                            c.get_nom() or '',
                            c.get_prenom() or '',
                            c.get_raison_sociale() or '',
                            c.get_courriel(),
                            c.get_status_client()
                        ))

                    def confirmer():
                        sel = tree_client.selection()
                        if not sel:
                            tk.messagebox.showwarning(
                                "Aucune sélection", "Veuillez sélectionner un client")
                            return
                        valeurs = tree_client.item(sel[0])['values']
                        client_selectionne_contrat['id'] = valeurs[0]
                        nom_affiche = valeurs[2] or valeurs[4]
                        client_var_contrat.set(f"{valeurs[0]} - {nom_affiche}")
                        popup_client.destroy()

                    ttk.Button(popup_client, text="✓ Choisir",
                               command=confirmer).pack(pady=10)

                ttk.Button(form, text="👤 Choisir un client", command=choisir_client_contrat).grid(
                    row=1, column=2, padx=5)

                ttk.Label(form, text="Date début :").grid(
                    row=2, column=0, sticky='w', pady=5)
                entry_debut = DateEntry(
                    form, width=28, date_pattern='yyyy-mm-dd')
                entry_debut.grid(row=2, column=1, pady=5, padx=5)

                ttk.Label(form, text="Durée :").grid(
                    row=3, column=0, sticky='w', pady=5)
                entry_duree = ttk.Entry(form, width=30)
                entry_duree.grid(row=3, column=1, pady=5, padx=5)

                ttk.Label(form, text="Nb productions :").grid(
                    row=4, column=0, sticky='w', pady=5)
                entry_nb = ttk.Entry(form, width=30)
                entry_nb.grid(row=4, column=1, pady=5, padx=5)

                ttk.Label(form, text="Périodicité :").grid(
                    row=5, column=0, sticky='w', pady=5)
                combo_periode = ttk.Combobox(form, width=28, state='readonly')
                combo_periode['values'] = (
                    'HEBDOMADAIRE', 'MENSUELLE', 'ANNUELLE')
                combo_periode.current(1)
                combo_periode.grid(row=5, column=1, pady=5, padx=5)

                ttk.Label(form, text="Montant global (€) :").grid(
                    row=6, column=0, sticky='w', pady=5)
                entry_montant = ttk.Entry(form, width=30)
                entry_montant.grid(row=6, column=1, pady=5, padx=5)

                ttk.Label(form, text="Conditions paiement :").grid(
                    row=7, column=0, sticky='w', pady=5)
                entry_conditions = ttk.Entry(form, width=30)
                entry_conditions.grid(row=7, column=1, pady=5, padx=5)

                btn_frame_creer = ttk.Frame(popup_creer)
                btn_frame_creer.pack(pady=15)

                def valider_contrat():
                    if not client_selectionne_contrat['id']:
                        tk.messagebox.showwarning(
                            "Client manquant", "Veuillez sélectionner un client")
                        return

                    duree = entry_duree.get().strip()
                    nb = entry_nb.get().strip()
                    montant = entry_montant.get().strip()
                    conditions = entry_conditions.get().strip()
                    debut = str(entry_debut.get_date())

                    if not duree or not nb or not montant or not conditions:
                        tk.messagebox.showwarning(
                            "Champs manquants", "Veuillez remplir tous les champs")
                        return
                    try:
                        nb_i = int(nb)
                        montant_f = float(montant)
                    except ValueError:
                        tk.messagebox.showwarning(
                            "Valeur invalide", "Nb productions et montant doivent être numériques")
                        return

                    from domaine.Contrat import Contrat
                    nouveau = Contrat(numero_contrat_auto, debut, duree, nb_i,
                                      combo_periode.get(), montant_f, conditions,
                                      # ← id du client choisi
                                      client_selectionne_contrat['id'])
                    cle = DAOContrat.get_instance().insert_contrat(nouveau)

                    if cle != -1:
                        tk.messagebox.showinfo(
                            "Succès", f"Contrat {numero_contrat_auto} créé !")
                        popup_creer.destroy()
                        charger_contrats()
                    else:
                        tk.messagebox.showerror(
                            "Erreur", "Impossible de créer le contrat")

                ttk.Button(btn_frame_creer, text="✓ Valider",
                           command=valider_contrat).pack(side='left', padx=5)
                ttk.Button(btn_frame_creer, text="✗ Annuler",
                           command=popup_creer.destroy).pack(side='left', padx=5)

            def confirmer():
                sel = tree_contrat.selection()
                if not sel:
                    tk.messagebox.showwarning(
                        "Aucune sélection", "Veuillez sélectionner un contrat")
                    return
                numero_contrat = tree_contrat.item(sel[0])['values'][0]
                popup_contrat.destroy()
                _sauvegarder(numero_contrat, date_acceptation, 'ACCEPTE')

            btn_frame_contrat = ttk.Frame(popup_contrat)
            btn_frame_contrat.pack(pady=10)
            ttk.Button(btn_frame_contrat, text="✓ Choisir ce contrat",
                       command=confirmer).pack(side='left', padx=5)
            ttk.Button(btn_frame_contrat, text="➕ Créer un contrat",
                       command=creer_contrat).pack(side='left', padx=5)

        def valider():
            nouveau_statut = combo_statut.get()
            date_acceptation = str(
                date.today()) if nouveau_statut == 'ACCEPTE' else None

            if nouveau_statut == 'ACCEPTE':
                _choisir_et_lier_contrat(date_acceptation)
                return

            _sauvegarder(values[7] or None, date_acceptation, nouveau_statut)

        ttk.Button(btn_frame, text="✓ Valider",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler",
                   command=popup.destroy).pack(side='left', padx=5)
'''
    # ------------------------------------------------------------------ #


    # ------------------------------------------------------------------ #
#numeroContrat, dateDebut, duree, nbProductionsTotales, periodicite, montantGlobal, conditionsPaiement, idClient


