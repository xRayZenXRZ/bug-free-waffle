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