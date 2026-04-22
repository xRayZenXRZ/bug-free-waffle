import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from dao.DAOUtilisateur import DAOUtilisateur

class ConnexionUI(tk.Frame):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.on_success = on_success_callback
        self.leDAOUtilisateur = DAOUtilisateur.get_instance()

        # Widgets
        self.label_email = ttk.Label(self, text="Email : ")
        self.entry_email = ttk.Entry(self)
        self.label_mdp = ttk.Label(self, text="Mot de passe : ")
        self.entry_mdp = ttk.Entry(self, show="*")
        self.bouton = ttk.Button(self, text="Valider", command=self.verification)

        # Packs
        self.label_email.pack(side='top', anchor='center', pady=(50, 5))
        self.entry_email.pack(side='top', anchor='center', pady=(0, 25))
        self.label_mdp.pack(side='top', anchor='center', pady=(25, 5))
        self.entry_mdp.pack(side='top', anchor='center', pady=(0, 50))
        self.bouton.pack(side='top', anchor='center', pady=(0, 75))

    def verification(self):
        email = self.entry_email.get()
        mdp = self.entry_mdp.get()

        if not email:
            mb.showwarning("Champs Vide", "Veuillez renseigner votre email")
            return

        if not mdp:
            mb.showwarning("Champs Vide", "Veuillez renseigner votre mot de passe")
            return

        if "@" not in email or "." not in email:
            mb.showwarning("Erreur", "Email non valide")
            return

        utilisateur = self.leDAOUtilisateur.find_by_email_motDePasse(email, mdp)

        if not utilisateur:
            self.entry_email.delete(0, tk.END)
            self.entry_mdp.delete(0, tk.END)
            mb.showwarning("Identifiant FAUX !", "Email ou mot de passe incorrect.")
            return
        else:
            mb.showinfo("Accès Granted", f"Bienvenue {utilisateur.get_prenom()} !")
            self.on_success(utilisateur)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Com'Art")
    root.geometry("800x400")
    app = ConnexionUI(root, lambda user: print(f"Connecté: {user}"))
    root.mainloop()
