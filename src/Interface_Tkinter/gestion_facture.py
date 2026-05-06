import tkinter as tk
from tkinter import ttk
from dao.DAOFacture import DAOFacture
from domaine.Facture import Facture
from datetime import date
from tkcalendar import DateEntry


class GestionFacture(tk.Frame):
    def __init__(self, parent, utilisateur, on_back=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur

        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)
        ttk.Label(
            header,
            text=f"Gestion des Factures - {utilisateur['prenom']} {utilisateur['nom']}",
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

        ttk.Button(frame_gauche, text="👁️ Voir les factures",
                   command=self.afficher_facture).pack(pady=5, fill='x')
        
        ttk.Button(frame_gauche, text="➕ Créer une facture",
                   command=self.faire_facture).pack(pady=5, fill='x')
        
        ttk.Button(frame_gauche, text="✏️ Modifier état",
                   command=self.changer_etat_facture).pack(pady=5, fill='x')
       
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(frame_gauche, text="🗑️ Supprimer facture",
                       command=self.supprimer_facture).pack(pady=5, fill='x')
        if on_back:
            ttk.Label(frame_gauche, text="").pack(expand=True)
            ttk.Button(frame_gauche, text="🏠 Accueil", command=on_back).pack(
                pady=5, fill='x', side='bottom')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)
        ttk.Label(frame_droite, text="Liste des factures :",
                  font=('Arial', 12, 'bold')).pack(pady=5)

        colonnes = ('Numéro Facture', 'Date Émission', 'Montant Total', 'État', 'Numéro Contrat')
        self.tree = ttk.Treeview(
            frame_droite, columns=colonnes, show='headings', height=15)

        for col in colonnes:
            self.tree.heading(col, text=col)

        self.tree.column('Numéro Facture', width=120, anchor='center')
        self.tree.column('Date Émission', width=120, anchor='center')
        self.tree.column('Montant Total', width=100, anchor='center')
        self.tree.column('État', width=100, anchor='center')
        self.tree.column('Numéro Contrat', width=120, anchor='center')

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
        self.afficher_facture()

    # ------------------------------------------------------------------ #

    def afficher_facture(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        facture_liste = DAOFacture.get_instance().select_facture()

        for f in facture_liste:
            self.tree.insert('', 'end', values=(
                f.get_numero_facture(),
                f.get_date_emission(),
                f"{f.get_montant_total()} €",
                f.get_etat(),
                f.get_numero_contrat(),
            ))
        print(f"{len(facture_liste)} facture(s) affichée(s)")
        
    # ------------------------------------------------------------------ #
    
    def supprimer_facture(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning(
                "Aucune sélection", "Veuillez sélectionner une facture")
            return

        values = self.tree.item(selection[0])['values']
        numero = values[0]

        reponse = tk.messagebox.askyesno(
            "Confirmation", f"Voulez-vous vraiment supprimer la facture « {numero} » ?")

        if reponse:
            f = Facture(numero, None, None, None, None)
            succes = DAOFacture.get_instance().delete_facture(f)
            if succes:
                self.tree.delete(selection[0])
                tk.messagebox.showinfo("Succès", "Facture supprimée")
            else:
                tk.messagebox.showerror("Erreur", "Impossible de supprimer la facture")


    # ------------------------------------------------------------------ #
    
    def changer_etat_facture(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning(
                "Aucune sélection", "Veuillez sélectionner une facture")
            return

        values = self.tree.item(selection[0])['values']
        numero_facture = values[0]
        etat_actuel = values[3]

        popup = tk.Toplevel(self)
        popup.title("Modifier l'état")
        popup.geometry("320x180")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Facture : {numero_facture}", font=(
            'Arial', 12, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10)

        ttk.Label(form_frame, text="État :").grid(
            row=0, column=0, sticky='w', pady=5)
        combo_etat = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_etat['values'] = ('EN_ATTENTE', 'PAYEE', 'ANNULEE', 'EN_RETARD')
        combo_etat.set(etat_actuel)
        combo_etat.grid(row=0, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            nouvel_etat = combo_etat.get()
            
            try:
                # On retire le symbole " €" pour récupérer le montant en float
                montant_str = str(values[2]).replace(' €', '')
                montant = float(montant_str)
            except ValueError:
                montant = 0.0
                
            # Reconstruction de la Facture avec ses nouvelles valeurs
            modifie = Facture(
                numero_facture,
                str(values[1]),
                montant,
                nouvel_etat,
                str(values[4]) if values[4] else None
            )
            
            succes = DAOFacture.get_instance().update_facture(modifie)
            if succes:
                tk.messagebox.showinfo(
                    "Succès", f"État de la facture {numero_facture} mis à jour !")
                popup.destroy()
                self.afficher_facture()
            else:
                tk.messagebox.showerror(
                    "Erreur", "Impossible de modifier l'état de la facture")

        ttk.Button(btn_frame, text="✓ Valider",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler",
                   command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def faire_facture(self):
        if hasattr(self, '_popup_ajout') and self._popup_ajout and self._popup_ajout.winfo_exists():
            self._popup_ajout.focus()
            return

        popup = tk.Toplevel(self)
        self._popup_ajout = popup
        popup.title("Créer une facture")
        popup.geometry("480x400")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        def generer_numero():
            annee = date.today().year
            facture_liste = DAOFacture.get_instance().select_facture()
            numeros = [
                f.get_numero_facture() for f in facture_liste
                if f.get_numero_facture() and str(annee) in f.get_numero_facture()
            ]
            if numeros:
                dernier = max(numeros)
                try:
                    numero_seq = int(dernier.split('-')[-1]) + 1
                except ValueError:
                    numero_seq = 1
            else:
                numero_seq = 1
            return f"FACT-{annee}-{numero_seq:03d}"

        numero_auto = generer_numero()

        ttk.Label(popup, text="Créer une nouvelle facture",
                  font=('Arial', 14, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        ttk.Label(form_frame, text="Numéro facture :").grid(
            row=0, column=0, sticky='w', pady=5)
        ttk.Label(form_frame, text=numero_auto, foreground='blue').grid(
            row=0, column=1, sticky='w', pady=5, padx=5)

        ttk.Label(form_frame, text="Contrat :").grid(
            row=1, column=0, sticky='w', pady=5)
        contrat_var = tk.StringVar(value="Aucun contrat sélectionné")
        ttk.Label(form_frame, textvariable=contrat_var, foreground='blue').grid(
            row=1, column=1, sticky='w', pady=5, padx=5)
        contrat_selectionne = {'numero': None}

        def choisir_contrat():
            from dao.DAOContrat import DAOContrat
            popup_contrat = tk.Toplevel(popup)
            popup_contrat.title("Choisir un contrat")
            popup_contrat.geometry("600x300")
            popup_contrat.transient(popup)
            popup_contrat.grab_set()

            ttk.Label(popup_contrat, text="Sélectionnez un contrat :",
                      font=('Arial', 12, 'bold')).pack(pady=10)

            cols = ('Numéro', 'Date début', 'Durée', 'Montant', 'Client ID')
            tree_contrat = ttk.Treeview(
                popup_contrat, columns=cols, show='headings', height=8)
            for col in cols:
                tree_contrat.heading(col, text=col)
            tree_contrat.column('Numéro', width=110, anchor='center')
            tree_contrat.column('Date début', width=90, anchor='center')
            tree_contrat.column('Durée', width=70, anchor='center')
            tree_contrat.column('Montant', width=80, anchor='center')
            tree_contrat.column('Client ID', width=60, anchor='center')
            tree_contrat.pack(fill='both', expand=True, padx=10)

            contrats = DAOContrat.get_instance().select_contrat()
            for c in contrats:
                tree_contrat.insert('', 'end', values=(
                    c.get_numero_contrat(),
                    c.get_date_debut(),
                    c.get_duree(),
                    f"{c.get_montant_global()} €",
                    c.get_id_client()
                ))

            def confirmer():
                sel = tree_contrat.selection()
                if not sel:
                    tk.messagebox.showwarning(
                        "Aucune sélection", "Veuillez sélectionner un contrat")
                    return
                valeurs = tree_contrat.item(sel[0])['values']
                contrat_selectionne['numero'] = valeurs[0]
                contrat_var.set(f"{valeurs[0]}")
                popup_contrat.destroy()

            ttk.Button(popup_contrat, text="✓ Choisir",
                       command=confirmer).pack(pady=10)

        ttk.Button(form_frame, text="📄 Choisir",
                   command=choisir_contrat).grid(row=1, column=2, padx=5)

        ttk.Label(form_frame, text="Date émission :").grid(
            row=2, column=0, sticky='w', pady=5)
        entry_emission = DateEntry(
            form_frame, width=28, date_pattern='yyyy-mm-dd')
        entry_emission.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Montant Total (€) :").grid(
            row=3, column=0, sticky='w', pady=5)
        entry_montant = ttk.Entry(form_frame, width=30)
        entry_montant.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="État :").grid(
            row=4, column=0, sticky='w', pady=5)
        combo_etat = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_etat['values'] = ('EN_ATTENTE', 'PAYEE')
        combo_etat.current(0)
        combo_etat.grid(row=4, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            numero = numero_auto
            num_contrat = contrat_selectionne['numero']
            emission = entry_emission.get_date()
            montant_str = entry_montant.get().strip()
            etat = combo_etat.get()

            # 1. Vérifier qu'un contrat a bien été sélectionné
            if not num_contrat:
                tk.messagebox.showwarning(
                    "Champs manquants", "Veuillez sélectionner un contrat")
                return

            if not montant_str:
                tk.messagebox.showwarning(
                    "Champs manquants", "Veuillez saisir un montant")
                return

            try:
                montant_f = float(montant_str)
            except ValueError:
                tk.messagebox.showwarning(
                    "Valeur invalide", "Le montant doit être numérique")
                return

            nouveau = Facture(numero, str(emission), montant_f, etat, num_contrat)
            
            succes = DAOFacture.get_instance().insert_facture(nouveau)
            
            # 2. Sécuriser la vérification du retour du DAO
            if succes and succes != -1:
                tk.messagebox.showinfo("Succès", "Facture créée avec succès !")
                popup.destroy()
                self.afficher_facture()
            else:
                tk.messagebox.showerror("Erreur", "Impossible de créer la facture")

        ttk.Button(btn_frame, text="✓ Valider",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler",
                   command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #
    
    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            tk.messagebox.showinfo("Détails facture", (
                f"Numéro    : {values[0]}\n"
                f"Date d'émission    : {values[1]}\n"
                f"Montant Total    : {values[2]}\n"
                f"État    : {values[3]}\n"
                f"Numéro Contrat    : {values[4]}"
            ))