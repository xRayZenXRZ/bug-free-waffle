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
    