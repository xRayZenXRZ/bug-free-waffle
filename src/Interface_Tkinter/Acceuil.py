import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

compte_utilisateur = {
    "Aled": {"email": "root@gmail.com", "mdp": "root"}
}


class ConnexionUI(tk.Frame):  # Hérite de Frame au lieu de rien
    def __init__(self, parent, on_success_callback):  # Prend parent et callback
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.on_success = on_success_callback  # Stocke le callback

        # Création email, mdp, bouton connexion :
        # self au lieu de self.root
        self.label_email = ttk.Label(self, text="Email : ")
        self.entry_email = ttk.Entry(self)
        self.label_mdp = ttk.Label(self, text="Mot de passe : ")
        self.entry_mdp = ttk.Entry(self, show="*")
        self.bouton = ttk.Button(self, text="Valider",
                                 command=self.verification)

        # Packs :
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
            mb.showwarning(
                "Champs Vide", "Veuillez renseigner votre mot de passe")
            return

        if not ("@" in email and "." in email):
            mb.showwarning("Erreur", "Email non valide")
            return

        # Chercher l'utilisateur
        valid = {client for client, identifiant in compte_utilisateur.items()
                 if identifiant["email"] == email and identifiant["mdp"] == mdp}

        if len(valid) <= 0:
            self.entry_email.delete(0, tk.END)
            self.entry_mdp.delete(0, tk.END)
            mb.showwarning("Identifiant FAUX !", "Veuillez réessayer.")
            return

        # mb.showinfo("Accès Granted", "Yayyyyyyyyyy !")

        # Récupérer le nom de l'utilisateur
        nom_utilisateur = list(valid)[0]

        # Appeler le callback pour passer à la page suivante
        self.on_success(nom_utilisateur, email)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Com'Art")
    root.geometry("800x400")
    app = ConnexionUI(root, lambda nom, email: print(f"Connecté: {nom}"))
    root.mainloop()
