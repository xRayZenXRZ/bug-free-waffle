import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import mysql.connector

class ConnexionUI(tk.Frame):  # Hérite de Frame au lieu de rien
    def __init__(self, parent, on_success_callback):  # Prend parent et callback
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.on_success = on_success_callback  # Stocke le callback

        #widgets : 
        self.label_email = ttk.Label(self, text="Email : ")
        self.entry_email = ttk.Entry(self)
        self.label_mdp = ttk.Label(self, text="Mot de passe : ")
        self.entry_mdp = ttk.Entry(self, show="*")
        self.bouton = ttk.Button(self, text="Valider", command=self.verification)

        # Packs :
        self.label_email.pack(side='top', anchor='center', pady=(50, 5))
        self.entry_email.pack(side='top', anchor='center', pady=(0, 25))
        self.label_mdp.pack(side='top', anchor='center', pady=(25, 5))
        self.entry_mdp.pack(side='top', anchor='center', pady=(0, 50))
        self.bouton.pack(side='top', anchor='center', pady=(0, 75))

    def connecter_bdd(self):
        """Connexion à la base de données"""
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Ton user MySQL
            password="",  # Ton mot de passe MySQL
            database="test_comart"
        )

    def verification(self):
        email = self.entry_email.get()
        mdp = self.entry_mdp.get()

        if not email:
            mb.showwarning("Champs Vide", "Veuillez renseigner votre email")
            return

        if not mdp:
            mb.showwarning(
                "Champs Vide", "Veuillez renseigner votre mot de passe")
            return

        if "@" not in email or "." not in email:
            mb.showwarning("Erreur", "Email non valide")
            return

        try:
            # Connexion à la BDD
            conn = self.connecter_bdd()
            cursor = conn.cursor(dictionary=True)

            # Requête pour vérifier l'utilisateur
            query = """
                SELECT idUtilisateur, nom, prenom, email, role, statut 
                FROM Utilisateur 
                WHERE email = %s AND motDePasse = %s AND statut = 'ACTIF'
            """
            cursor.execute(query, (email, mdp))
            utilisateur = cursor.fetchone()

            cursor.close()
            conn.close()

            if not utilisateur:
                self.entry_email.delete(0, tk.END)
                self.entry_mdp.delete(0, tk.END)
                mb.showwarning("Identifiant FAUX !", "Email ou mot de passe incorrect.")
                return
    
            mb.showinfo("Accès Granted", f"Bienvenue {utilisateur['prenom']} !")
            # Passer toutes les infos utilisateur
            self.on_success(utilisateur)

        except mysql.connector.Error as err:
            mb.showerror("Erreur BDD", f"Erreur de connexion : {err}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Com'Art")
    root.geometry("800x400")
    app = ConnexionUI(root, lambda user: print(f"Connecté: {user}"))
    root.mainloop()
