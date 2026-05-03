import tkinter as tk
from tkinter import ttk
from dao.DAODevis import DAODevis
from dao.DAOClient import DAOClient
import tkinter.messagebox
from domaine.Devis import Devis
from datetime import date
from tkcalendar import DateEntry
from dao.DAOContrat import DAOContrat

class GestionDevis(tk.Frame):
    def __init__(self, parent, utilisateur, on_back=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur

        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)
        ttk.Label(
            header,
            text=f"Gestion des Devis - {utilisateur['prenom']} {utilisateur['nom']}",
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
        ttk.Button(frame_gauche, text="➕ Créer un devis",    command=self.ajouter_devis).pack(pady=5, fill='x')
        ttk.Button(frame_gauche, text="👁️ Voir les devis",   command=self.afficher_devis).pack(pady=5, fill='x')
        ttk.Button(frame_gauche, text="✏️ Modifier statut",  command=self.modifier_statut).pack(pady=5, fill='x')
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(frame_gauche, text="🗑️ Supprimer devis", command=self.supprimer_devis).pack(pady=5, fill='x')

        if on_back:
            ttk.Label(frame_gauche, text="").pack(expand=True)
            ttk.Button(frame_gauche, text="🏠 Accueil", command=on_back).pack(pady=5, fill='x', side='bottom')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)
        ttk.Label(frame_droite, text="Liste des devis :", font=('Arial', 12, 'bold')).pack(pady=5)

        colonnes = ('Numéro', 'Date émission', 'Date validité', 'Description', 'Montant', 'Statut', 'Client', 'Contrat')
        self.tree = ttk.Treeview(frame_droite, columns=colonnes, show='headings', height=15)

        for col in colonnes:
            self.tree.heading(col, text=col)

        self.tree.column('Numéro',        width=110, anchor='center')
        self.tree.column('Date émission', width=100, anchor='center')
        self.tree.column('Date validité', width=100, anchor='center')
        self.tree.column('Description',   width=200, anchor='w')
        self.tree.column('Montant',       width=80,  anchor='center')
        self.tree.column('Statut',        width=90,  anchor='center')
        self.tree.column('Client',        width=60,  anchor='center')
        self.tree.column('Contrat',       width=110, anchor='center')

        # Scrollbar horizontale
        scrollbar_x = ttk.Scrollbar(frame_droite, orient='horizontal', command=self.tree.xview)
        scrollbar_x.pack(side='bottom', fill='x')

        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(frame_droite, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(fill='both', expand=True)

        self.tree.bind('<Double-1>', self.on_double_click)
        self.afficher_devis()

    # ------------------------------------------------------------------ #

    def afficher_devis(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        devis_liste = DAODevis.get_instance().select_devis()

        for d in devis_liste:
            self.tree.insert('', 'end', values=(
                d.get_numero_devis(),
                d.get_date_emission(),
                d.get_date_validite(),
                d.get_description_prestation(),
                f"{d.get_montant_total_estime()} €",
                d.get_statut(),
                d.get_id_client(),
                d.get_numero_contrat() or ''
            ))
        print(f"{len(devis_liste)} devis affiché(s)")

    # ------------------------------------------------------------------ #

    def ajouter_devis(self):
        if hasattr(self, '_popup_ajout') and self._popup_ajout and self._popup_ajout.winfo_exists():
            self._popup_ajout.focus()
            return

        popup = tk.Toplevel(self)
        self._popup_ajout = popup
        popup.title("Créer un devis")
        popup.geometry("480x520")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()


        # Générer le numéro automatiquement
        def generer_numero():
            annee = date.today().year
            devis_liste = DAODevis.get_instance().select_devis()
            # Trouver le dernier numéro de l'année en cours
            numeros = [
                d.get_numero_devis() for d in devis_liste
                if d.get_numero_devis() and str(annee) in d.get_numero_devis()
            ]
            if numeros:
                dernier = max(numeros)  # ex: DEV-2026-009
                numero_seq = int(dernier.split('-')[-1]) + 1
            else:
                numero_seq = 1
            return f"DEV-{annee}-{numero_seq:03d}"  # ← format DEV-2026-001

        numero_auto = generer_numero()
        
        ttk.Label(popup, text="Créer un nouveau devis", font=('Arial', 14, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Numéro devis
        ttk.Label(form_frame, text="Numéro devis :").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Label(form_frame, text=numero_auto, foreground='blue').grid(row=0, column=1, sticky='w', pady=5, padx=5)

        # Client
        ttk.Label(form_frame, text="ID Client :").grid(row=1, column=0, sticky='w', pady=5)
        entry_client = ttk.Entry(form_frame, width=30)
        entry_client.grid(row=1, column=1, pady=5, padx=5)

        # Description
        ttk.Label(form_frame, text="Description :").grid(row=2, column=0, sticky='w', pady=5)
        entry_desc = ttk.Entry(form_frame, width=30)
        entry_desc.grid(row=2, column=1, pady=5, padx=5)

        # Quantité
        ttk.Label(form_frame, text="Quantité :").grid(row=3, column=0, sticky='w', pady=5)
        entry_qte = ttk.Entry(form_frame, width=30)
        entry_qte.insert(0, "1")
        entry_qte.grid(row=3, column=1, pady=5, padx=5)

        # Détails coûts
        ttk.Label(form_frame, text="Détails coûts :").grid(row=4, column=0, sticky='w', pady=5)
        entry_couts = ttk.Entry(form_frame, width=30)
        entry_couts.grid(row=4, column=1, pady=5, padx=5)

        # Montant
        ttk.Label(form_frame, text="Montant (€) :").grid(row=5, column=0, sticky='w', pady=5)
        entry_montant = ttk.Entry(form_frame, width=30)
        entry_montant.grid(row=5, column=1, pady=5, padx=5)

        # Remplacez les Entry de date par :
        ttk.Label(form_frame, text="Date émission :").grid(row=6, column=0, sticky='w', pady=5)
        entry_emission = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
        entry_emission.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date validité :").grid(row=7, column=0, sticky='w', pady=5)
        entry_validite = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
        entry_validite.grid(row=7, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Contrat :").grid(row=8, column=0, sticky='w', pady=5)

        contrat_var = tk.StringVar(value="Aucun contrat sélectionné")
        lbl_contrat = ttk.Label(form_frame, textvariable=contrat_var, foreground='blue')
        lbl_contrat.grid(row=8, column=1, sticky='w', pady=5, padx=5)

        contrat_selectionne = {'numero': None}  # ← stocke le choix

        def choisir_contrat():
            popup_contrat = tk.Toplevel(popup)
            popup_contrat.title("Choisir un contrat")
            popup_contrat.geometry("600x300")
            popup_contrat.transient(popup)
            popup_contrat.grab_set()

            ttk.Label(popup_contrat, text="Sélectionnez un contrat :", font=('Arial', 12, 'bold')).pack(pady=10)

            # Treeview des contrats
            cols = ('Numéro', 'Date début', 'Durée', 'Périodicité', 'Montant', 'Client')
            tree_contrat = ttk.Treeview(popup_contrat, columns=cols, show='headings', height=8)
            for col in cols:
                tree_contrat.heading(col, text=col)
            tree_contrat.column('Numéro',      width=110, anchor='center')
            tree_contrat.column('Date début',  width=90,  anchor='center')
            tree_contrat.column('Durée',       width=70,  anchor='center')
            tree_contrat.column('Périodicité', width=90,  anchor='center')
            tree_contrat.column('Montant',     width=80,  anchor='center')
            tree_contrat.column('Client',      width=60,  anchor='center')
            tree_contrat.pack(fill='both', expand=True, padx=10)

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

            def confirmer():
                selection = tree_contrat.selection()
                if not selection:
                    tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un contrat")
                    return
                valeurs = tree_contrat.item(selection[0])['values']
                contrat_selectionne['numero'] = valeurs[0]
                contrat_var.set(valeurs[0])  # ← met à jour le label
                popup_contrat.destroy()

            ttk.Button(popup_contrat, text="✓ Choisir", command=confirmer).pack(pady=10)

        ttk.Button(form_frame, text="📋 Choisir un contrat", command=choisir_contrat).grid(row=2, column=2, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            numero = numero_auto
            id_client = entry_client.get().strip()
            desc     = entry_desc.get().strip()
            qte      = entry_qte.get().strip()
            couts    = entry_couts.get().strip()
            montant  = entry_montant.get().strip()
            emission = entry_emission.get_date()
            validite = entry_validite.get_date()
            numero_contrat = contrat_selectionne['numero']  # None si pas sélectionné

            if validite <= emission:
                tk.messagebox.showwarning("Date invalide", "La date de validité doit être après la date d'émission")
                return

            if emission < date.today():
                tk.messagebox.showwarning("Date invalide", "La date d'émission ne peut pas être dans le passé")
                return
            statut = 'EN_ATTENTE'

            if not numero or not id_client or not desc or not montant or not emission or not validite:
                tk.messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs obligatoires")
                return

            try:
                montant_f = float(montant)
                qte_i = int(qte)
                id_client_i = int(id_client)
            except ValueError:
                tk.messagebox.showwarning("Valeur invalide", "Montant, quantité et ID client doivent être numériques")
                return


            nouveau = Devis(numero, str(entry_emission.get_date()), str(entry_validite.get_date()), desc, qte_i, couts, montant_f, statut, None, id_client_i, numero_contrat)
            cle = DAODevis.get_instance().insert_devis(nouveau)

            if cle != -1:
                tk.messagebox.showinfo("Succès", "Devis créé avec succès !")
                popup.destroy()
                self.afficher_devis()
            else:
                tk.messagebox.showerror("Erreur", "Impossible de créer le devis")

        ttk.Button(btn_frame, text="✓ Valider",  command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler", command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def modifier_statut(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un devis")
            return

        values = self.tree.item(selection[0])['values']
        # values : (Numéro, Date émission, Date validité, Description, Montant, Statut, Client, Contrat)

        popup = tk.Toplevel(self)
        popup.title("Modifier le statut")
        popup.geometry("320x180")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Devis : {values[0]}", font=('Arial', 12, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10)

        ttk.Label(form_frame, text="Statut :").grid(row=0, column=0, sticky='w', pady=5)
        combo_statut = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_statut['values'] = ('EN_ATTENTE', 'ACCEPTE', 'REFUSE', 'EXPIRE')
        combo_statut.set(values[5])
        combo_statut.grid(row=0, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():

            nouveau_statut = combo_statut.get()
            # Date d'acceptation automatique si statut ACCEPTE
            date_acceptation = str(date.today()) if nouveau_statut == 'ACCEPTE' else None

            modifie = Devis(
                values[0],
                str(values[1]),
                str(values[2]),
                str(values[3]),
                1,
                "",
                float(str(values[4]).replace(' €', '')),
                nouveau_statut,
                date_acceptation,  # ← automatique
                int(values[6]),
                values[7] or None
            )
            succes = DAODevis.get_instance().update_devis(modifie)
            if succes:
                tk.messagebox.showinfo("Succès", f"Statut du devis {values[0]} mis à jour !")
                popup.destroy()
                self.afficher_devis()
            else:
                tk.messagebox.showerror("Erreur", "Impossible de modifier le statut")

        ttk.Button(btn_frame, text="✓ Valider",  command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler", command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def supprimer_devis(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un devis")
            return

        values = self.tree.item(selection[0])['values']
        numero = values[0]

        reponse = tk.messagebox.askyesno(
            "Confirmation", f"Voulez-vous vraiment supprimer le devis « {numero} » ?")

        if reponse:
            d = Devis(numero, None, None, None, None, None, None, None, None, None, None)
            succes = DAODevis.get_instance().delete_devis(d)
            if succes:
                self.tree.delete(selection[0])
                tk.messagebox.showinfo("Succès", "Devis supprimé")
            else:
                tk.messagebox.showerror("Erreur", "Impossible de supprimer le devis")

    # ------------------------------------------------------------------ #

    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            tk.messagebox.showinfo("Détails devis", (
                f"Numéro      : {values[0]}\n"
                f"Émission    : {values[1]}\n"
                f"Validité    : {values[2]}\n"
                f"Description : {values[3]}\n"
                f"Montant     : {values[4]}\n"
                f"Statut      : {values[5]}\n"
                f"Client ID   : {values[6]}\n"
                f"Contrat     : {values[7]}"
            ))