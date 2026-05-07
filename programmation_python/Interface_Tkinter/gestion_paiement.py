"""Onglet de gestion des paiements — enregistrement des versements liés aux factures."""

import tkinter as tk
from tkinter import ttk
from dao.DAOPaiement import DAOPaiement
from dao.DAOFacture import DAOFacture
from domaine.Paiement import Paiement
from datetime import date
from tkcalendar import DateEntry

class GestionPaiement(tk.Frame):
    def __init__(self, parent, utilisateur, on_back=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur

        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)
        ttk.Label(
            header,
            text=f"Gestion des Paiements - {utilisateur['prenom']} {utilisateur['nom']}",
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

        ttk.Button(frame_gauche, text="Voir les paiements",
                   command=self.afficher_paiements).pack(pady=5, fill='x')
        
        ttk.Button(frame_gauche, text="Enregistrer un paiement",
                   command=self.faire_paiement).pack(pady=5, fill='x')
        
        ttk.Button(frame_gauche, text="Modifier le paiement",
                   command=self.modifier_paiement).pack(pady=5, fill='x')
       
        if utilisateur['role'] == 'ADMIN':
            ttk.Button(frame_gauche, text="Supprimer paiement",
                       command=self.supprimer_paiement).pack(pady=5, fill='x')
        if on_back:
            ttk.Label(frame_gauche, text="").pack(expand=True)
            ttk.Button(frame_gauche, text="Accueil", command=on_back).pack(
                pady=5, fill='x', side='bottom')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)
        ttk.Label(frame_droite, text="Liste des paiements :",
                  font=('Arial', 12, 'bold')).pack(pady=5)

        colonnes = ('ID Paiement', 'Date', 'Montant', 'Numéro Facture')
        self.tree = ttk.Treeview(
            frame_droite, columns=colonnes, show='headings', height=15)

        for col in colonnes:
            self.tree.heading(col, text=col)

        self.tree.column('ID Paiement', width=100, anchor='center')
        self.tree.column('Date', width=120, anchor='center')
        self.tree.column('Montant', width=120, anchor='center')
        self.tree.column('Numéro Facture', width=150, anchor='center')

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
        self.afficher_paiements()

    def afficher_paiements(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        paiements_liste = DAOPaiement.get_instance().select_paiement()

        for p in paiements_liste:
            self.tree.insert('', 'end', values=(
                p.get_id_paiement(),
                p.get_date(),
                f"{p.get_montant()} €",
                p.get_numero_facture(),
            ))
        print(f"{len(paiements_liste)} paiement(s) affiché(s)")

    def supprimer_paiement(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un paiement")
            return

        values = self.tree.item(selection[0])['values']
        id_paiement = values[0]

        reponse = tk.messagebox.askyesno(
            "Confirmation", f"Voulez-vous vraiment supprimer le paiement N°{id_paiement} ?")

        if reponse:
            p = Paiement(id_paiement, None, None, None)
            succes = DAOPaiement.get_instance().delete_paiement(p)
            if succes:
                self.tree.delete(selection[0])
                tk.messagebox.showinfo("Succès", "Paiement supprimé")
            else:
                tk.messagebox.showerror("Erreur", "Impossible de supprimer le paiement")

    def faire_paiement(self):
        if hasattr(self, '_popup_ajout') and self._popup_ajout and self._popup_ajout.winfo_exists():
            self._popup_ajout.focus()
            return

        popup = tk.Toplevel(self)
        self._popup_ajout = popup
        popup.title("Enregistrer un paiement")
        popup.geometry("480x300")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text="Nouveau paiement",
                  font=('Arial', 14, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        ttk.Label(form_frame, text="Facture :").grid(row=0, column=0, sticky='w', pady=5)
        facture_var = tk.StringVar(value="Aucune facture sélectionnée")
        ttk.Label(form_frame, textvariable=facture_var, foreground='blue').grid(
            row=0, column=1, sticky='w', pady=5, padx=5)
        # On garde en mémoire le numéro de la facture ET son reste à payer
        facture_selectionnee = {'numero': None, 'reste_a_payer': 0}

        def choisir_facture():
            popup_fact = tk.Toplevel(popup)
            popup_fact.title("Choisir une facture")
            popup_fact.geometry("600x300")
            popup_fact.transient(popup)
            popup_fact.grab_set()

            ttk.Label(popup_fact, text="Sélectionnez une facture :", font=('Arial', 12, 'bold')).pack(pady=10)

            cols = ('Numéro', 'Date', 'Montant Restant', 'État')
            tree_fact = ttk.Treeview(popup_fact, columns=cols, show='headings', height=8)
            for col in cols:
                tree_fact.heading(col, text=col)
            tree_fact.pack(fill='both', expand=True, padx=10)

            factures = DAOFacture.get_instance().select_facture()
            tous_les_paiements = DAOPaiement.get_instance().select_paiement()
            
            for f in factures:
                # Calcul simple du reste à payer pour chaque facture
                total_deja_paye = 0
                for p in tous_les_paiements:
                    if p.get_numero_facture() == f.get_numero_facture():
                        total_deja_paye = total_deja_paye + p.get_montant()
                
                montant_restant = f.get_montant_total() - total_deja_paye
                if montant_restant < 0:
                    montant_restant = 0  # Pour ne pas avoir de montant négatif
                    
                tree_fact.insert('', 'end', values=(
                    f.get_numero_facture(),
                    f.get_date_emission(),
                    f"{int(montant_restant)} €", 
                    f.get_etat()
                ))

            def confirmer():
                sel = tree_fact.selection()
                if not sel:
                    tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une facture")
                    return
                valeurs = tree_fact.item(sel[0])['values']
                facture_selectionnee['numero'] = valeurs[0]
                
                # On enlève le texte "€" pour sauvegarder juste le nombre
                reste_str = str(valeurs[2]).replace(' €', '')
                facture_selectionnee['reste_a_payer'] = float(reste_str)
                
                facture_var.set(f"{valeurs[0]} (Reste : {valeurs[2]})")
                popup_fact.destroy()

            ttk.Button(popup_fact, text="Choisir", command=confirmer).pack(pady=10)

        ttk.Button(form_frame, text="Choisir", command=choisir_facture).grid(row=0, column=2, padx=5)

        ttk.Label(form_frame, text="Date paiement :").grid(row=1, column=0, sticky='w', pady=5)
        entry_date = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
        entry_date.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Montant (€) :").grid(row=2, column=0, sticky='w', pady=5)
        entry_montant = ttk.Entry(form_frame, width=30)
        entry_montant.grid(row=2, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            num_facture = facture_selectionnee['numero']
            date_paiement = entry_date.get_date()
            montant_str = entry_montant.get().strip()

            if not num_facture:
                tk.messagebox.showwarning("Champs manquants", "Veuillez sélectionner une facture")
                return
            if not montant_str:
                tk.messagebox.showwarning("Champs manquants", "Veuillez saisir un montant")
                return
            try:
                montant_f = float(montant_str)
            except ValueError:
                tk.messagebox.showwarning("Valeur invalide", "Le montant doit être numérique")
                return

            # Si on essaie de payer plus que ce qu'il reste à payer on affiche impossible
            if montant_f > facture_selectionnee['reste_a_payer']:
                tk.messagebox.showwarning(
                    "Montant trop grand", 
                    f"Erreur ! Vous essayez d'enregistrer {montant_f} € mais il ne reste que {facture_selectionnee['reste_a_payer']} € à payer.")
                return

            nouveau = Paiement(None, str(date_paiement), montant_f, num_facture)

            if nouveau.get_id_paiement() and nouveau.get_id_paiement() != -1:
                tk.messagebox.showinfo("Succès", "Paiement enregistré avec succès !")
                popup.destroy()
                self.afficher_paiements()
            else:
                tk.messagebox.showerror("Erreur", "Impossible d'enregistrer le paiement")

        ttk.Button(btn_frame, text="Valider", command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Annuler", command=popup.destroy).pack(side='left', padx=5)

    def modifier_paiement(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un paiement à modifier")
            return

        values = self.tree.item(selection[0])['values']
        id_paiement = values[0]
        date_actuelle = str(values[1])
        montant_actuel = str(values[2]).replace(' €', '')
        facture_actuelle = str(values[3])
        
        def calculer_reste_pour_facture(num_facture, id_paiement_ignore):
            la_facture = DAOFacture.get_instance().find_facture(num_facture)
            if la_facture is None:
                return 0
                
            somme_paiements = 0
            for p in DAOPaiement.get_instance().select_paiement():
                if p.get_numero_facture() == num_facture:
                    if p.get_id_paiement() != id_paiement_ignore:
                        somme_paiements = somme_paiements + p.get_montant()
                        
            reste = la_facture.get_montant_total() - somme_paiements
            if reste < 0:
                reste = 0
            return reste
            
        reste_initial = calculer_reste_pour_facture(facture_actuelle, id_paiement)
        facture_selectionnee = {'numero': facture_actuelle, 'reste_a_payer': reste_initial}

        popup = tk.Toplevel(self)
        popup.title("Modifier un paiement")
        popup.geometry("480x300")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Modifier le paiement N°{id_paiement}",
                  font=('Arial', 14, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        ttk.Label(form_frame, text="Facture :").grid(row=0, column=0, sticky='w', pady=5)
        facture_var = tk.StringVar(value=f"{facture_actuelle} (Reste : {int(reste_initial)} €)")
        ttk.Label(form_frame, textvariable=facture_var, foreground='blue').grid(
            row=0, column=1, sticky='w', pady=5, padx=5)

        def choisir_facture():
            popup_fact = tk.Toplevel(popup)
            popup_fact.title("Choisir une facture")
            popup_fact.geometry("600x300")
            popup_fact.transient(popup)
            popup_fact.grab_set()

            ttk.Label(popup_fact, text="Sélectionnez une facture :", font=('Arial', 12, 'bold')).pack(pady=10)

            cols = ('Numéro', 'Date', 'Montant Restant', 'État')
            tree_fact = ttk.Treeview(popup_fact, columns=cols, show='headings', height=8)
            for col in cols:
                tree_fact.heading(col, text=col)
            tree_fact.pack(fill='both', expand=True, padx=10)

            factures = DAOFacture.get_instance().select_facture()
            for f in factures:
                reste = calculer_reste_pour_facture(f.get_numero_facture(), id_paiement)
                tree_fact.insert('', 'end', values=(
                    f.get_numero_facture(), 
                    f.get_date_emission(), 
                    f"{int(reste)} €", 
                    f.get_etat()
                ))

            def confirmer():
                sel = tree_fact.selection()
                if not sel:
                    tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une facture")
                    return
                valeurs = tree_fact.item(sel[0])['values']
                facture_selectionnee['numero'] = valeurs[0]
                
                reste_str = str(valeurs[2]).replace(' €', '')
                facture_selectionnee['reste_a_payer'] = float(reste_str)
                
                facture_var.set(f"{valeurs[0]} (Reste : {valeurs[2]})")
                popup_fact.destroy()

            ttk.Button(popup_fact, text="Choisir", command=confirmer).pack(pady=10)

        ttk.Button(form_frame, text="Choisir", command=choisir_facture).grid(row=0, column=2, padx=5)

        ttk.Label(form_frame, text="Date paiement :").grid(row=1, column=0, sticky='w', pady=5)
        entry_date = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
        try:
            entry_date.set_date(date.fromisoformat(date_actuelle))
        except ValueError:
            pass
        entry_date.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Montant (€) :").grid(row=2, column=0, sticky='w', pady=5)
        entry_montant = ttk.Entry(form_frame, width=30)
        entry_montant.insert(0, montant_actuel)
        entry_montant.grid(row=2, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            num_facture = facture_selectionnee['numero']
            date_paiement = entry_date.get_date()
            montant_str = entry_montant.get().strip()

            if not num_facture or not montant_str:
                tk.messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs")
                return
            try:
                montant_f = float(montant_str)
            except ValueError:
                tk.messagebox.showwarning("Valeur invalide", "Le montant doit être numérique")
                return
                
            if montant_f > facture_selectionnee['reste_a_payer']:
                tk.messagebox.showwarning(
                    "Montant trop grand", 
                    f"Erreur ! Vous essayez d'enregistrer {montant_f} € mais il ne reste que {facture_selectionnee['reste_a_payer']} € à payer.")
                return

            modifie = Paiement(id_paiement, str(date_paiement), montant_f, num_facture)
            
            succes = DAOPaiement.get_instance().update_paiement(modifie)
            if succes:
                tk.messagebox.showinfo("Succès", "Paiement modifié avec succès !")
                popup.destroy()
                self.afficher_paiements()
            else:
                tk.messagebox.showerror("Erreur", "Impossible de modifier le paiement")

        ttk.Button(btn_frame, text="Valider", command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Annuler", command=popup.destroy).pack(side='left', padx=5)

    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            tk.messagebox.showinfo("Détails paiement", (
                f"ID Paiement    : {values[0]}\n"
                f"Date Paiement  : {values[1]}\n"
                f"Montant Payé   : {values[2]}\n"
                f"Numéro Facture : {values[3]}"
            ))