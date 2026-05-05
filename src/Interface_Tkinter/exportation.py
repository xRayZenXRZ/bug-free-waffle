import csv
import pandas as pd

from domaine.Activite import Activite
from domaine.Collaborateur import Collaborateur
from domaine.Paiement import Paiement
from domaine.Client import Client
from domaine.Contrat import Contrat
from domaine.Devis import Devis
from domaine.Facture import Facture
from domaine.Prestation import Prestation


# Exportations individuelles 

def exportation_clients_csv(client=None):
    clients = Client.leDAOClient.select_client(client)
    fichier_csv = "src/Interface_Tkinter/exportation/client/clients.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["idClient", "type_client", "nom", "prenom",
                         "raisonSociale", "adressePostale", "telephone", "email", "statut"])
        for x in clients:
            type_client = "ENTREPRISE" if x.get_raison_sociale() is not None else "PARTICULIER"
            writer.writerow([
                x.get_id_client(), type_client, x.get_nom(), x.get_prenom(),
                x.get_raison_sociale(), x.get_adresse(), x.get_telephone(),
                x.get_courriel(), x.get_status_client()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_prestations_csv(prestation=None):
    prestations = Prestation.leDAOPrestation.select_prestation(prestation)
    fichier_csv = "src/Interface_Tkinter/exportation/prestation/prestations.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["idPrestation", "datePrevue", "dateEffective", "lieu",
                         "type", "nbPhotosPrevues", "nbVideosPrevues", "numeroContrat"])
        for x in prestations:
            writer.writerow([
                x.get_id_prestation(), x.get_date_prevue(), x.get_date_effective(),
                x.get_lieu(), x.get_type(), x.get_nb_photos_prevues(),
                x.get_nb_videos_prevues(), x.get_numero_contrat()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportations_factures_csv(facture=None):
    factures = Facture.leDAOFacture.select_facture(facture)
    fichier_csv = "src/Interface_Tkinter/exportation/facture/factures.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["numeroFacture", "dateEmission", "montantTotal", "etat", "numeroContrat"])
        for x in factures:
            writer.writerow([
                x.get_numero_facture(), x.get_date_emission(),
                x.get_montant_total(), x.get_etat(), x.get_numero_contrat()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_contrat_csv(contrat=None):
    contrats = Contrat.leDAOContrat.select_contrat(contrat)
    fichier_csv = "src/Interface_Tkinter/exportation/contrat/contrats.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["numeroContrat", "dateDebut", "duree", "nbProductionsTotales",
                         "periodicite", "montantGlobal", "conditionsPaiement", "idClient"])
        for x in contrats:
            writer.writerow([
                x.get_numero_contrat(), x.get_date_debut(), x.get_duree(),
                x.get_nb_productions_totales(), x.get_periodicite(),
                x.get_montant_global(), x.get_condition_paiements(), x.get_id_client()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_devis_csv(devis=None):
    liste_devis = Devis.leDAODevis.select_devis(devis)  # ← nom différent du paramètre
    fichier_csv = "src/Interface_Tkinter/exportation/devis/devis.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["numeroDevis", "dateEmission", "dateValidite", "descriptionPrestation",
                         "quantitePrevue", "detailsCouts", "montantTotalEstime", "statut",
                         "dateAcceptation", "idClient", "numeroContrat"])
        for x in liste_devis:
            writer.writerow([
                x.get_numero_devis(), x.get_date_emission(), x.get_date_validite(),
                x.get_description_prestation(), x.get_quantite_prevue(), x.get_details_couts(),
                x.get_montant_total_estime(), x.get_statut(), x.get_date_acceptation(),
                x.get_id_client(), x.get_numero_contrat()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_paiement_csv(paiement=None):
    paiements = Paiement.leDAOPaiement.select_paiement(paiement)
    fichier_csv = "src/Interface_Tkinter/exportation/paiement/paiements.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["idPaiement", "datePaiement", "montantPaye", "numeroFacture"])
        for x in paiements:
            writer.writerow([
                x.get_id_paiement(), x.get_date(),
                x.get_montant(), x.get_numero_facture()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_activite_csv(activite=None):
    activites = Activite.leDAOActivite.select_activite(activite)
    fichier_csv = "src/Interface_Tkinter/exportation/activite/activites.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["idActivite", "libelleOperationnel", "datePrevue", "dateEffective",
                         "dureeEstimeeHeures", "statut", "idPrestation", "idCollaborateur"])
        for x in activites:
            writer.writerow([
                x.get_id_activite(), x.get_libelle_operationnel(), x.get_date_prevues(),
                x.get_date_effective(), x.get_duree_estimee(), x.get_statut(),
                x.get_id_prestation(), x.get_id_collaborateur()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_collaborateur_csv(collaborateur=None): 
    collaborateurs = Collaborateur.leDAOCollaborateur.select_collaborateur(collaborateur)
    fichier_csv = "src/Interface_Tkinter/exportation/collaborateur/collaborateurs.csv"

    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["idCollaborateur", "nom", "prenom", "poste",
                         "telephonePro", "numeroDevis", "idUtilisateur"])
        for x in collaborateurs:
            writer.writerow([
                x.get_id_collaborateur(), x.get_nom(), x.get_prenom(), x.get_poste(),
                x.get_telephone_pro(), x.get_numero_devis(), x.get_id_utilisateur()
            ])

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


#  Export global  

def exportation_all_csv():
    exportation_collaborateur_csv()
    exportation_clients_csv()
    exportation_activite_csv()
    exportation_contrat_csv()
    exportation_devis_csv()
    exportation_paiement_csv()
    exportations_factures_csv()
    exportation_prestations_csv()


#  Vues combinées

def exportation_combined_csv():
    dossier = "src/Interface_Tkinter/exportation"

    clients        = pd.read_csv(f"{dossier}/client/clients.csv",             sep=";", encoding="utf-8")
    contrats       = pd.read_csv(f"{dossier}/contrat/contrats.csv",           sep=";", encoding="utf-8")
    devis          = pd.read_csv(f"{dossier}/devis/devis.csv",                sep=";", encoding="utf-8")
    prestations    = pd.read_csv(f"{dossier}/prestation/prestations.csv",     sep=";", encoding="utf-8")
    factures       = pd.read_csv(f"{dossier}/facture/factures.csv",           sep=";", encoding="utf-8")
    paiements      = pd.read_csv(f"{dossier}/paiement/paiements.csv",         sep=";", encoding="utf-8")
    activites      = pd.read_csv(f"{dossier}/activite/activites.csv",         sep=";", encoding="utf-8")
    collaborateurs = pd.read_csv(f"{dossier}/collaborateur/collaborateurs.csv", sep=";", encoding="utf-8")

    # Normalisation des types pour les jointures
    for df, col in [
        (activites,      "idCollaborateur"),
        (collaborateurs, "idCollaborateur"),
        (contrats,       "idClient"),
        (clients,        "idClient"),
        (prestations,    "numeroContrat"),
        (contrats,       "numeroContrat"),
        (factures,       "numeroContrat"),
        (devis,          "idClient"),
        (devis,          "numeroContrat"),
        (paiements,      "numeroFacture"),
        (factures,       "numeroFacture"),
    ]:
        df[col] = df[col].astype(str)

    # Vue contrats + client
    contrats_clients = contrats.merge(
        clients[["idClient", "nom", "prenom", "raisonSociale", "email", "telephone"]],
        on="idClient", how="left"
    )

    # Vue prestations complètes
    prestations_full = prestations.merge(contrats_clients, on="numeroContrat", how="left")

    # Vue activités complètes
    activites_full = activites.merge(
        prestations_full[["idPrestation", "lieu", "type", "numeroContrat"]],
        on="idPrestation", how="left"
    ).merge(
        collaborateurs[["idCollaborateur", "nom", "prenom", "poste"]],
        on="idCollaborateur", how="left",
        suffixes=("_activite", "_collaborateur")
    )

    # Vue factures complètes
    factures_full = factures.merge(contrats_clients, on="numeroContrat", how="left")

    # Vue paiements complets
    paiements_full = paiements.merge(
        factures_full[["numeroFacture", "montantTotal", "etat", "idClient"]],
        on="numeroFacture", how="left"
    )

    # Vue devis complets
    devis_full = devis.merge(
        clients[["idClient", "nom", "prenom", "raisonSociale"]],
        on="idClient", how="left"
    ).merge(
        contrats[["numeroContrat", "montantGlobal", "periodicite"]],
        on="numeroContrat", how="left"
    )

    # Export
    dossier_sortie = f"{dossier}/combined"
    vues = {
        "contrats_clients":  contrats_clients,
        "prestations_full":  prestations_full,
        "activites_full":    activites_full,
        "factures_full":     factures_full,
        "paiements_full":    paiements_full,
        "devis_full":        devis_full,
    }

    for nom, df in vues.items():
        chemin = f"{dossier_sortie}/{nom}.csv"
        df.to_csv(chemin, index=False, sep=";", encoding="utf-8")
        print(f"Le fichier {chemin} a été créé avec succès.")


def exportation_contrats_clients_combined_csv(id_client: int = None):
    chemin = "src/Interface_Tkinter/exportation/combined/contrats_clients.csv"
    contrats_clients = pd.read_csv(chemin, sep=";", encoding="utf-8")

    if id_client is not None:
        contrats_clients = contrats_clients[contrats_clients["idClient"] == int(id_client)]

    output_path = "src/Interface_Tkinter/exportation/combined/byclient/contrats_clients.csv"
    contrats_clients.to_csv(output_path, index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {output_path} via id_client a été créé avec succès.")


if __name__ == "__main__":
    exportation_combined_csv()