from domaine.Activite import Activite
from domaine.Collaborateur import Collaborateur
from domaine.Paiement import Paiement
from domaine.Client import Client
from domaine.Contrat import Contrat
from domaine.Devis import Devis
from domaine.Facture import Facture
from domaine.Prestation import Prestation
import pandas as pd

import csv


def exportation_clients_csv(client=None):

    clients = Client.leDAOClient.select_client(client)

    fichier_texte = "src/Interface_Tkinter/exportation/client/clients.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/client/clients.csv"
    
    with open(fichier_texte, "w", encoding="utf=8") as client_file : 
        client_file.write("idClient;type_client;nom;prenom;raisonSociale;adressePostale;telephone;email;statut")
        for x in clients : 
            if(x.get_raison_sociale() is not None) :
                ligne = (f"{x.get_id_client()};ENTREPRISE;{x.get_nom()};{x.get_prenom()};{x.get_raison_sociale()};{x.get_adresse()};{x.get_telephone()};{x.get_courriel()};{x.get_status_client()}").strip()
                client_file.write("\n"+ligne)
            else : 
                ligne = (f"{x.get_id_client()};PARTICULIER;{x.get_nom()};{x.get_prenom()};{x.get_raison_sociale()};{x.get_adresse()};{x.get_telephone()};{x.get_courriel()};{x.get_status_client()}").strip()
                client_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as client_file : 
        lignes = client_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as client_file_csv:
        writer = csv.writer(client_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportation_prestations_csv(prestation=None):
    
    prestations = Prestation.leDAOPrestation.select_prestation(prestation)

    fichier_texte = "src/Interface_Tkinter/exportation/prestation/prestations.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/prestation/prestations.csv"

    with open(fichier_texte, "w", encoding="utf=8") as prestation_file : 
        prestation_file.write("idPrestation;datePrevue;dateEffective;lieu;type;nbPhotosPrevues;nbVideosPrevues;numeroContrat")
        for x in prestations : 
            ligne = (f"{x.get_id_prestation()};{x.get_date_prevue()};{x.get_date_effective()};{x.get_lieu()};{x.get_type()};{x.get_nb_photos_prevues()};{x.get_nb_videos_prevues()};{x.get_numero_contrat()}").strip()
            prestation_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as prestation_file : 
        lignes = prestation_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as prestation_file_csv:
        writer = csv.writer(prestation_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportations_factures_csv(facture=None):

    factures = Facture.leDAOFacture.select_facture(facture)

    fichier_texte = "src/Interface_Tkinter/exportation/facture/factures.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/facture/factures.csv"

    with open(fichier_texte, "w", encoding="utf=8") as facture_file : 
        facture_file.write("numeroFacture;dateEmission;montantTotal;etat;numeroContrat")
        for x in factures : 
            ligne = (f"{x.get_numero_facture()};{x.get_date_emission()};{x.get_montant_total()};{x.get_etat()};{x.get_numero_contrat()}").strip()
            facture_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as facture_file : 
        lignes = facture_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as facture_file_csv:
        writer = csv.writer(facture_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportation_contrat_csv(contrat=None):

    contrats = Contrat.leDAOContrat.select_contrat(contrat)

    fichier_texte = "src/Interface_Tkinter/exportation/contrat/contrats.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/contrat/contrats.csv"

    with open(fichier_texte, "w", encoding="utf=8") as contrat_file : 
        contrat_file.write("numeroContrat;dateDebut;duree;nbProductionsTotales;periodicite;montantGlobal;conditionsPaiement;idClient")
        for x in contrats :
            ligne = (f"{x.get_numero_contrat()};{x.get_date_debut()};{x.get_duree()};{x.get_nb_productions_totales()};{x.get_periodicite()};{x.get_montant_global()};{x.get_condition_paiements()};{x.get_id_client()}").strip()
            contrat_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as contrat_file : 
        lignes = contrat_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as contrat_file_csv:
        writer = csv.writer(contrat_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportation_devis_csv(devis=None):

    devis = Devis.leDAODevis.select_devis(devis)

    fichier_texte = "src/Interface_Tkinter/exportation/devis/devis.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/devis/devis.csv"

    with open(fichier_texte, "w", encoding="utf=8") as devis_file : 
        devis_file.write("numeroDevis;dateEmission;dateValidite;descriptionPrestation;quantitePrevue;detailsCouts;montantTotalEstime;statut;dateAcceptation;idClient;numeroContrat")
        for x in devis :
            ligne = (f"{x.get_numero_devis()};{x.get_date_emission()};{x.get_date_validite()};{x.get_description_prestation()};{x.get_quantite_prevue()};{x.get_details_couts()};{x.get_montant_total_estime()};{x.get_statut()};{x.get_date_acceptation()};{x.get_id_client()};{x.get_numero_contrat()}").strip()
            devis_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as devis_file : 
        lignes = devis_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as devis_file_csv:
        writer = csv.writer(devis_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportation_paiement_csv(paiement=None):

    paiements = Paiement.leDAOPaiement.select_paiement(paiement)

    fichier_texte = "src/Interface_Tkinter/exportation/paiement/paiements.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/paiement/paiements.csv"

    with open(fichier_texte, "w", encoding="utf=8") as paiement_file : 
        paiement_file.write("idPaiement;datePaiement;montantPaye;numeroFacture")
        for x in paiements :
            ligne = (f"{x.get_id_paiement()};{x.get_date()};{x.get_montant()};{x.get_numero_facture()}").strip()
            paiement_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as paiement_file : 
        lignes = paiement_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as paiement_file_csv:
        writer = csv.writer(paiement_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportation_activite_csv(activite=None):

    activites = Activite.leDAOActivite.select_activite(activite)

    fichier_texte = "src/Interface_Tkinter/exportation/activite/activites.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/activite/activites.csv"

    with open(fichier_texte, "w", encoding="utf=8") as activite_file : 
        activite_file.write("idActivite;libelleOperationnel;datePrevue;dateEffective;dureeEstimeeHeures;statut;idPrestation;idCollaborateur")
        for x in activites :
            ligne = (f"{x.get_id_activite()};{x.get_libelle_operationnel()};{x.get_date_prevues()};{x.get_date_effective()};{x.get_duree_estimee()};{x.get_statut()};{x.get_id_prestation()};{x.get_id_collaborateur()}")
            activite_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as activite_file : 
        lignes = activite_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as activite_file_csv:
        writer = csv.writer(activite_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def exportation_collaborateur_csv(collaboratuer=None):

    collaborateurs = Collaborateur.leDAOCollaborateur.select_collaborateur(collaboratuer)

    fichier_texte = "src/Interface_Tkinter/exportation/collaborateur/collaborateurs.txt"
    fichier_csv = "src/Interface_Tkinter/exportation/collaborateur/collaborateurs.csv"

    with open(fichier_texte, "w", encoding="utf=8") as collaborateur_file : 
        collaborateur_file.write("idCollaborateur;nom;prenom;poste;telephonePro;numeroDevis;idUtilisateur")
        for x in collaborateurs :
            ligne = (f"{x.get_id_collaborateur()};{x.get_nom()};{x.get_prenom()};{x.get_poste()};{x.get_telephone_pro()};{x.get_numero_devis()};{x.get_id_utilisateur()}").strip()
            collaborateur_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as collaborateur_file : 
        lignes = collaborateur_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as collaborateur_file_csv:
        writer = csv.writer(collaborateur_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def exportation_all_csv():
    exportation_collaborateur_csv()
    exportation_clients_csv()
    exportation_activite_csv()
    exportation_contrat_csv()
    exportation_devis_csv()
    exportation_paiement_csv()
    exportations_factures_csv()
    exportation_prestations_csv()


import pandas as pd

def exportation_contrats_clients_combined_csv(id_client : int):

    contrats_clients = pd.read_csv("src/Interface_Tkinter/exportation/combined/contrats_clients.csv", sep=";", encoding="utf-8-sig")
    
    # Filter by id_client if provided
    if id_client is not None:
        filtered_contrat_clients = contrats_clients[contrats_clients["idClient"] == int(id_client)]
    else:
        # If no id_client is provided, keep all rows
        filtered_contrat_clients = contrats_clients

    # Save combined CSV
    output_path = "src/Interface_Tkinter/exportation/combined/byclient/contrats_clients.csv"
    filtered_contrat_clients.to_csv(output_path, index=False, sep=";", encoding="utf-8")

    print(f"Le fichier {output_path} via id_client a été créé avec succès.")


def exportation_combined_csv():

    clients       = pd.read_csv(f"src/Interface_Tkinter/exportation/client/clients.csv",             sep=",", encoding="utf-8")
    contrats      = pd.read_csv(f"src/Interface_Tkinter/exportation/contrat/contrats.csv",           sep=",", encoding="utf-8")
    devis         = pd.read_csv(f"src/Interface_Tkinter/exportation/devis/devis.csv",                sep=",", encoding="utf-8")
    prestations   = pd.read_csv(f"src/Interface_Tkinter/exportation/prestation/prestations.csv",     sep=",", encoding="utf-8")
    factures      = pd.read_csv(f"src/Interface_Tkinter/exportation/facture/factures.csv",           sep=",", encoding="utf-8")
    paiements     = pd.read_csv(f"src/Interface_Tkinter/exportation/paiement/paiements.csv",         sep=",", encoding="utf-8")
    activites     = pd.read_csv(f"src/Interface_Tkinter/exportation/activite/activites.csv",         sep=",", encoding="utf-8")
    collaborateurs = pd.read_csv(f"src/Interface_Tkinter/exportation/collaborateur/collaborateurs.csv", sep=",", encoding="utf-8")

    # Vue contrats (contrat + client)
    contrats_clients = contrats.merge(clients[["idClient", "nom", "prenom", "raisonSociale", "email", "telephone"]], on="idClient", how="left")

    # Vue prestations (prestation + contrat + client)
    prestations_full = prestations.merge(contrats_clients, on="numeroContrat", how="left")

    # csv -> str 
    activites["idCollaborateur"]      = activites["idCollaborateur"].astype(str)
    collaborateurs["idCollaborateur"] = collaborateurs["idCollaborateur"].astype(str)
    contrats["idClient"]              = contrats["idClient"].astype(str)
    clients["idClient"]               = clients["idClient"].astype(str)
    prestations["numeroContrat"]      = prestations["numeroContrat"].astype(str)
    contrats["numeroContrat"]         = contrats["numeroContrat"].astype(str)
    factures["numeroContrat"]         = factures["numeroContrat"].astype(str)
    devis["idClient"]                 = devis["idClient"].astype(str)
    devis["numeroContrat"]            = devis["numeroContrat"].astype(str)
    paiements["numeroFacture"]        = paiements["numeroFacture"].astype(str)
    factures["numeroFacture"]         = factures["numeroFacture"].astype(str)

    # Vue activités (activite + prestation + collaborateur) 
    activites_full = activites.merge( prestations_full[["idPrestation", "lieu", "type", "numeroContrat"]], on="idPrestation", how="left"
    ).merge(
        collaborateurs[["idCollaborateur", "nom", "prenom", "poste"]],
        on="idCollaborateur", how="left",
        suffixes=("_activite", "_collaborateur")
    )

    # Vue factures complètes (facture + contrat + client + paiements) 
    factures_full = factures.merge(contrats_clients, on="numeroContrat", how="left")
    paiements_full = paiements.merge(
        factures_full[["numeroFacture", "montantTotal", "etat", "idClient"]],
        on="numeroFacture", how="left"
    )

    # Vue devis (devis + client + contrat)
    devis_full = devis.merge( clients[["idClient", "nom", "prenom", "raisonSociale"]], on="idClient", how="left"
    ).merge(
        contrats[["numeroContrat", "montantGlobal", "periodicite"]], on="numeroContrat", how="left"
    )

    #export

    dossier_sortie = "src/Interface_Tkinter/exportation/combined"

    contrats_clients.to_csv(f"{dossier_sortie}/contrats_clients.csv", index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {dossier_sortie}/contrats_clients.csv a été créé avec succès.")

    prestations_full.to_csv(f"{dossier_sortie}/prestations_full.csv", index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {dossier_sortie}/prestations_full.csv a été créé avec succès.")

    activites_full.to_csv(f"{dossier_sortie}/activites_full.csv", index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {dossier_sortie}/activites_full.csv a été créé avec succès.")

    factures_full.to_csv(f"{dossier_sortie}/factures_full.csv", index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {dossier_sortie}/factures_full.csv a été créé avec succès.")

    paiements_full.to_csv(f"{dossier_sortie}/paiements_full.csv", index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {dossier_sortie}/paiements_full.csv a été créé avec succès.")

    devis_full.to_csv(f"{dossier_sortie}/devis_full.csv", index=False, sep=";", encoding="utf-8")
    print(f"Le fichier {dossier_sortie}/devis_full.csv a été créé avec succès.")

if __name__ == "__main__" :
    exportation_contrats_clients_combined_csv(id_client=4)