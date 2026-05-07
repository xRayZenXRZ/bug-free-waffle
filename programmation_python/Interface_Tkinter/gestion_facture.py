"""Onglet de facturation — génération de factures et consultation des montants dus."""

import tkinter as tk
from tkinter import ttk
from dao.DAOFacture import DAOFacture
from domaine.Facture import Facture
from datetime import date


class GestionFacture(tk.Frame):
    def __init__(self, parent, utilisateur, on_back=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur

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

        ttk.Button(frame_gauche, text="Voir les factures",
                   command=self.afficher_facture).pack(pady=5, fill='x')
        
        ttk.Button(frame_gauche, text="Modifier état",
                   command=self.changer_etat_facture).pack(pady=5, fill='x')
        
        ttk.Button(frame_gauche, text="Actualiser les factures",
                   command=self.generer_factures_manquantes).pack(pady=5, fill='x')
       
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(frame_gauche, text="Supprimer facture",
                       command=self.supprimer_facture).pack(pady=5, fill='x')
            ttk.Button(frame_gauche, text="Supprimer toutes les factures",
                       command=self.supprimer_toutes_factures).pack(pady=5, fill='x')
        if on_back:
            ttk.Label(frame_gauche, text="").pack(expand=True)
            ttk.Button(frame_gauche, text="Accueil", command=on_back).pack(
                pady=5, fill='x', side='bottom')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)
        ttk.Label(frame_droite, text="Liste des factures :",
                  font=('Arial', 12, 'bold')).pack(pady=5)

        colonnes = ('Numéro Facture', 'Date Émission', 'Montant Total', 'État', 'Numéro Contrat', 'Montant Restant')
        self.tree = ttk.Treeview(
            frame_droite, columns=colonnes, show='headings', height=15)

        for col in colonnes:
            self.tree.heading(col, text=col)

        self.tree.column('Numéro Facture', width=120, anchor='center')
        self.tree.column('Date Émission', width=120, anchor='center')
        self.tree.column('Montant Total', width=100, anchor='center')
        self.tree.column('État', width=100, anchor='center')
        self.tree.column('Numéro Contrat', width=120, anchor='center')
        self.tree.column('Montant Restant', width=120, anchor='center')

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

        from dao.DAOPaiement import DAOPaiement

        tous_paiements = DAOPaiement.get_instance().select_paiement()

        # Calculer le total payer par facture
        paiements_par_facture = {}
        for p in tous_paiements:
            num_f = p.get_numero_facture()
            if num_f:
                paiements_par_facture[num_f] = paiements_par_facture.get(num_f, 0) + p.get_montant()

        for f in facture_liste:
            num_f = f.get_numero_facture()
            total_paye = paiements_par_facture.get(num_f, 0)
            
            # Montant restant = Montant total de la facture - paiements, 0 minimum
            montant_restant = max(0, f.get_montant_total() - total_paye)
            
            # On détermine l'état en fonction du montant restant
            if montant_restant == 0:
                etat_logique = "PAYEE"
            elif montant_restant < f.get_montant_total():
                etat_logique = "PARTIELLEMENT_PAYEE"
            else:
                etat_logique = "EN_ATTENTE"
                
            # On met à jour l'état si nécessaire
            if f.get_etat() not in ["ANNULEE", "EN_RETARD"] and f.get_etat() != etat_logique:
                f.set_etat(etat_logique)

            self.tree.insert('', 'end', values=(
                f.get_numero_facture(),
                f.get_date_emission(),
                f"{int(f.get_montant_total())} €",
                f.get_etat(),
                f.get_numero_contrat(),
                f"{int(montant_restant)} €"
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
    
    def supprimer_toutes_factures(self):
        reponse = tk.messagebox.askyesno(
            "Avertissement critique", "Voulez-vous vraiment supprimer TOUTES les factures ?\n\nCette action est irréversible.")

        if reponse:
            factures = DAOFacture.get_instance().select_facture()
            erreurs = 0
            for f in factures:
                succes = DAOFacture.get_instance().delete_facture(f)
                if not succes:
                    erreurs += 1
            
            self.afficher_facture()
            if erreurs == 0:
                tk.messagebox.showinfo("Succès", "Toutes les factures ont été supprimées.")
            else:
                tk.messagebox.showwarning("Erreur partielle", f"{erreurs} facture(s) n'ont pas pu être supprimée(s).")

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
        combo_etat['values'] = ('EN_ATTENTE', 'PAYEE', 'PARTIELLEMENT_PAYEE', 'ANNULEE', 'EN_RETARD')
        combo_etat.set(etat_actuel)
        combo_etat.grid(row=0, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            nouvel_etat = combo_etat.get()
            
            try:
                montant_str = str(values[2]).replace(' €', '')
                montant = float(montant_str)
            except ValueError:
                montant = 0.0
                
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

        ttk.Button(btn_frame, text="Valider",
                   command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Annuler",
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
                f"Numéro Contrat    : {values[4]}\n"
                f"Montant Restant    : {values[5]}"
            ))

    # ------------------------------------------------------------------ #

    def generer_factures_manquantes(self):
        from dao.DAOContrat import DAOContrat

        contrats = DAOContrat.get_instance().select_contrat()
        factures_existantes = DAOFacture.get_instance().select_facture()
        numeros_contrats_avec_facture = {f.get_numero_contrat() for f in factures_existantes}

        annee = date.today().year
        numeros = [f.get_numero_facture() for f in factures_existantes if f.get_numero_facture() and str(annee) in f.get_numero_facture()]
        if numeros:
            try:
                dernier = int(max(numeros).split('-')[-1])
            except ValueError:
                dernier = 0
        else:
            dernier = 0

        nouvelles = 0

        for c in contrats:
            num_c = c.get_numero_contrat()
            if num_c in numeros_contrats_avec_facture:
                continue

            dernier += 1
            num_facture = f"FACT-{annee}-{dernier:03d}"
            nouvelle = Facture(num_facture, c.get_date_debut(), int(c.get_montant_global()), 'EN_ATTENTE', num_c)
            DAOFacture.get_instance().insert_facture(nouvelle)
            nouvelles += 1
                    
        if nouvelles > 0:
            tk.messagebox.showinfo("Succès", f"{nouvelles} nouvelle(s) facture(s) générée(s) avec succès !")
            self.afficher_facture()
        else:
            tk.messagebox.showinfo("Information", "Toutes les factures sont déjà à jour pour les contrats existants.")