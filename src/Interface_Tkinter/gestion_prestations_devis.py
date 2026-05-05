import tkinter as tk
from tkinter import ttk

from dao.DAOActivite import DAOActivite
from dao.DAOClient import DAOClient
from dao.DAOPrestation import DAOPrestation


class GestionPrestationActivite(tk.Frame):
    def __init__(self, parent, utilisateur):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.utilisateur = utilisateur
        
        # Notebook 
        onglets = ttk.Notebook(self)
        onglets.pack(fill="both", expand=True)
        
        # Pages
        page_clients = ttk.Frame(onglets)
        page_prestations = ttk.Frame(onglets)
        page_activites = ttk.Frame(onglets)

        onglets.add(page_clients, text="Gestion des Clients")
        onglets.add(page_prestations, text="Gestion des Prestations")
        onglets.add(page_activites, text="Gestion des Activités")
        
 
        # Treeview Clients
 
        self.tree_clients = self.create_treeview(
            page_clients,
            columns=('ID', 'Type', 'Nom', 'Prénom', 'Raison Sociale', 'Email', 'Téléphone', 'Statut'),
            heading="Liste des Clients"
        )

 
        # Treeview Prestations
 
        self.tree_prestations = self.create_treeview(
            page_prestations,
            columns=('ID', 'Date Prevue', 'Lieu', 'Type', 'nb Photos Prevues','nb Videos Prevues', 'Numero Contrat'),
            heading="Liste des Prestations"
        )

 
        # Treeview Activités
 
        self.tree_activites = self.create_treeview(
            page_activites,
            columns=('ID', 'libelle Operationnel', 'Date Prevue', 'Date Effective', 'dureeEstimeeHeures','statut', 'idCollaborateur', 'idPrestation' ),
            heading="Liste des Activités"
        )

        self.afficher_clients()
        self.afficher_prestations()
        self.afficher_activites()

    # Fonction utilitaire pour créer un Treeview

    def create_treeview(self, parent, columns, heading=""):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(frame, text=heading, font=('Arial', 12, 'bold')).pack(pady=5)

        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=100)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
        scrollbar_x.pack(side='bottom', fill='x')

        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        tree.pack(fill='both', expand=True)
        
        return tree


    def afficher_clients(self):
        tree = self.tree_clients
        for item in tree.get_children():
            tree.delete(item)

        clients = DAOClient.get_instance().select_client()

        for c in clients:
            tree.insert('', 'end', values=(
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

    # Affichage Prestations
    def afficher_prestations(self):
        tree = self.tree_prestations
        for item in tree.get_children():
            tree.delete(item)

        prestations = DAOPrestation.get_instance().select_prestation()

        for p in prestations:
            tree.insert('', 'end', values=(
                p.get_id_prestation(),
                p.get_date_prevue(),
                p.get_lieu(),
                p.get_type(),
                p.get_nb_photos_prevues(),
                p.get_nb_videos_prevues(),
                p.get_numero_contrat()
            ))
        print(f"{len(prestations)} prestation(s) affichée(s)")

    # Affichage Activités

    def afficher_activites(self):
        tree = self.tree_activites
        for item in tree.get_children():
            tree.delete(item)

        activites = DAOActivite.get_instance().select_activite()

        for a in activites:
            tree.insert('', 'end', values=(
                a.get_id_activite(),
                a.get_libelle_operationnel(),
                a.get_date_prevues(),
                a.get_date_effective(),
                a.get_duree_estimee(),
                a.get_statut(),
                a.get_id_collaborateur(),
                a.get_id_prestation()
            ))
        print(f"{len(activites)} activité(s) affichée(s)")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Gestion des Prestations et Activités")
    utilisateur = {"prenom":"Alice", "nom":"Dupont", "role":"ADMIN"}
    app = GestionPrestationActivite(root, utilisateur)
    app.pack(fill='both', expand=True)
    root.mainloop()