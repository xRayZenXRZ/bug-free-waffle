import tkinter as tk
from tkinter import ttk
from Interface_Tkinter.exportation import exportation_clients_csv
from dao.DAOClient import DAOClient
import tkinter.messagebox


class GestionClient(tk.Frame):
    def __init__(self, parent, utilisateur, on_back=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur

        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', pady=10)
        ttk.Label(
            header,
            text=f"Gestion des Clients - {utilisateur['prenom']} {utilisateur['nom']}",
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
        ttk.Button(frame_gauche, text="➕ Ajouter client",   command=self.ajouter_client).pack(pady=5, fill='x')
        ttk.Button(frame_gauche, text="👁️ Voir les clients", command=self.afficher_clients).pack(pady=5, fill='x')
        ttk.Button(frame_gauche, text="✏️ Modifier client",  command=self.modifier_client).pack(pady=5, fill='x')
        #ajouter d'exporatation : 
        ttk.Button(frame_gauche, text="Exportation", command=exportation_clients_csv).pack(pady = 5, fill ='x', side = 'bottom')

        if utilisateur['role'] == 'ADMIN':
            ttk.Button(frame_gauche, text="🗑️ Supprimer client", command=self.supprimer_client).pack(pady=5, fill='x')
            
        if on_back:
            ttk.Label(frame_gauche, text="").pack(expand=True)
            ttk.Button(
                frame_gauche,
                text="🏠 Accueil",
                command=on_back
            ).pack(pady=5, fill='x', side='bottom')

        # COLONNE DROITE : Tableau
        frame_droite = ttk.Frame(main_frame)
        frame_droite.pack(side='right', fill='both', expand=True, padx=10)
        ttk.Label(frame_droite, text="Liste des clients :", font=('Arial', 12, 'bold')).pack(pady=5)

        colonnes = ('ID', 'Type', 'Nom', 'Prénom', 'Raison Sociale', 'Email', 'Téléphone', 'Statut')
        self.tree = ttk.Treeview(frame_droite, columns=colonnes, show='headings', height=15)

        for col in colonnes:
            self.tree.heading(col, text=col)

        self.tree.column('ID',             width=40,  anchor='center')
        self.tree.column('Type',           width=90,  anchor='center')
        self.tree.column('Nom',            width=100, anchor='center')
        self.tree.column('Prénom',         width=100, anchor='center')
        self.tree.column('Raison Sociale', width=150, anchor='center')
        self.tree.column('Email',          width=180, anchor='center')
        self.tree.column('Téléphone',      width=100, anchor='center')
        self.tree.column('Statut',         width=80,  anchor='center')

        # Scrollbar horizontale — en premier (side='bottom')
        scrollbar_x = ttk.Scrollbar(frame_droite, orient='horizontal', command=self.tree.xview)
        scrollbar_x.pack(side='bottom', fill='x')

        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(frame_droite, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(fill='both', expand=True)  # ← en dernier

        self.tree.bind('<Double-1>', self.on_double_click)
        self.afficher_clients()

    # ------------------------------------------------------------------ #

    def afficher_clients(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        clients = DAOClient.get_instance().select_client()

        for c in clients:
            self.tree.insert('', 'end', values=(
                c.get_id_client(),
                'ENTREPRISE' if c.get_raison_sociale() else 'PARTICULIER',
                c.get_nom() or '',
                c.get_prenom() or '',
                c.get_raison_sociale() or '',
                c.get_courriel(),
                c.get_telephone() or '',
                c.get_status_client()
            ))
        print(f"{len(clients)} client(s) affiché(s)")

    def ajouter_client(self):
        if hasattr(self, '_popup_ajout') and self._popup_ajout and self._popup_ajout.winfo_exists():
            self._popup_ajout.focus()
            return
        popup = tk.Toplevel(self)
        self._popup_ajout = popup
        popup.title("Ajouter un client")
        popup.geometry("420x450")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text="Créer un nouveau client", font=('Arial', 14, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Type
        ttk.Label(form_frame, text="Type :").grid(row=0, column=0, sticky='w', pady=5)
        combo_type = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_type['values'] = ('PARTICULIER', 'ENTREPRISE')
        combo_type.current(0)
        combo_type.grid(row=0, column=1, pady=5, padx=5)

        # Champs PARTICULIER
        lbl_nom      = ttk.Label(form_frame, text="Nom :")
        entry_nom    = ttk.Entry(form_frame, width=30)
        lbl_prenom   = ttk.Label(form_frame, text="Prénom :")
        entry_prenom = ttk.Entry(form_frame, width=30)

        # Champs ENTREPRISE
        lbl_rs   = ttk.Label(form_frame, text="Raison Sociale :")
        entry_rs = ttk.Entry(form_frame, width=30)

        # Champs communs
        ttk.Label(form_frame, text="Adresse :").grid(row=4, column=0, sticky='w', pady=5)
        entry_adresse = ttk.Entry(form_frame, width=30)
        entry_adresse.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Email :").grid(row=5, column=0, sticky='w', pady=5)
        entry_email = ttk.Entry(form_frame, width=30)
        entry_email.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Téléphone :").grid(row=6, column=0, sticky='w', pady=5)
        entry_tel = ttk.Entry(form_frame, width=30)
        entry_tel.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Statut :").grid(row=7, column=0, sticky='w', pady=5)
        combo_statut = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_statut['values'] = ('PROSPECT', 'CLIENT', 'ANCIEN')
        combo_statut.current(0)
        combo_statut.grid(row=7, column=1, pady=5, padx=5)

        def maj_champs(event=None):
            lbl_nom.grid_remove()
            entry_nom.grid_remove()
            lbl_prenom.grid_remove()
            entry_prenom.grid_remove()
            lbl_rs.grid_remove()
            entry_rs.grid_remove()

            if combo_type.get() == 'PARTICULIER':
                lbl_nom.grid(row=1, column=0, sticky='w', pady=5)
                entry_nom.grid(row=1, column=1, pady=5, padx=5)
                lbl_prenom.grid(row=2, column=0, sticky='w', pady=5)
                entry_prenom.grid(row=2, column=1, pady=5, padx=5)
            else:
                lbl_rs.grid(row=1, column=0, sticky='w', pady=5)
                entry_rs.grid(row=1, column=1, pady=5, padx=5)

        combo_type.bind("<<ComboboxSelected>>", maj_champs)
        maj_champs()

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            type_client = combo_type.get()
            nom     = entry_nom.get().strip() or None
            prenom  = entry_prenom.get().strip() or None
            rs      = entry_rs.get().strip() or None
            adresse = entry_adresse.get().strip() or ""
            email   = entry_email.get().strip()
            tel     = entry_tel.get().strip() or None
            statut  = combo_statut.get()

            if not email or "@" not in email:
                tk.messagebox.showwarning("Email invalide", "Veuillez entrer un email valide")
                return
            if type_client == 'PARTICULIER' and (not nom or not prenom):
                tk.messagebox.showwarning("Champs manquants", "Nom et prénom obligatoires pour un particulier")
                return
            if type_client == 'ENTREPRISE' and not rs:
                tk.messagebox.showwarning("Champs manquants", "Raison sociale obligatoire pour une entreprise")
                return

            from domaine.Client import Client
            nouveau = Client(None, nom, prenom, rs, adresse, tel, email, statut)

            if nouveau.get_id_client() and nouveau.get_id_client() != -1:
                tk.messagebox.showinfo("Succès", "Client créé avec succès !")
                popup.destroy()
                self.afficher_clients()
            else:
                tk.messagebox.showerror("Erreur", "Impossible de créer le client")

        ttk.Button(btn_frame, text="✓ Valider",  command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler", command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def modifier_client(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client")
            return

        values = self.tree.item(selection[0])['values']
        nom_affiche = values[2] or values[4]

        popup = tk.Toplevel(self)
        popup.title("Modifier le statut")
        popup.geometry("320x200")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Client : {nom_affiche}", font=('Arial', 12, 'bold')).pack(pady=15)

        form_frame = ttk.Frame(popup)
        form_frame.pack(padx=20, pady=10)

        ttk.Label(form_frame, text="Statut :").grid(row=0, column=0, sticky='w', pady=5)
        combo_statut = ttk.Combobox(form_frame, width=28, state='readonly')
        combo_statut['values'] = ('PROSPECT', 'CLIENT', 'ANCIEN')
        combo_statut.set(values[7])
        combo_statut.grid(row=0, column=1, pady=5, padx=5)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def valider():
            from domaine.Client import Client
            modifie = Client(
                values[0],
                str(values[2]).strip() or "",
                str(values[3]).strip() or "",
                str(values[4]).strip() or "",
                "",
                str(values[6]).strip() or "",
                str(values[5]).strip(),
                combo_statut.get()
            )
            succes = DAOClient.get_instance().update_client(modifie)
            if succes:
                tk.messagebox.showinfo("Succès", f"Statut de {nom_affiche} mis à jour !")
                popup.destroy()
                self.afficher_clients()
            else:
                tk.messagebox.showerror("Erreur", "Impossible de modifier le statut")

        ttk.Button(btn_frame, text="✓ Valider",  command=valider).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✗ Annuler", command=popup.destroy).pack(side='left', padx=5)

    # ------------------------------------------------------------------ #

    def supprimer_client(self):
        selection = self.tree.selection()
        if not selection:
            tk.messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client")
            return

        values = self.tree.item(selection[0])['values']
        id_client = values[0]
        nom_affiche = values[2] or values[4]

        reponse = tk.messagebox.askyesno(
            "Confirmation", f"Voulez-vous vraiment supprimer « {nom_affiche} » ?")

        if reponse:
            from domaine.Client import Client
            c = Client(id_client, "", "", "", "", "", "", "")
            succes = DAOClient.get_instance().delete_client(c)
            if succes:
                self.tree.delete(selection[0])
                tk.messagebox.showinfo("Succès", "Client supprimé")
            else:
                tk.messagebox.showerror("Erreur", "Impossible de supprimer le client")

    # ------------------------------------------------------------------ #

    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            tk.messagebox.showinfo(
                "Détails",
                f"Client sélectionné : {item['values']}"
            )
