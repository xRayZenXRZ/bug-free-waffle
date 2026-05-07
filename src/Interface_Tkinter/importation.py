import csv
from dao.DAOSession import DAOSession
from dao.DAOClient import DAOClient
from dao.DAOCollaborateur import DAOCollaborateur
from dao.DAOContrat import DAOContrat
from dao.DAODevis import DAODevis
from dao.DAOPrestation import DAOPrestation
from dao.DAOFacture import DAOFacture
from dao.DAOActivite import DAOActivite
from dao.DAOPaiement import DAOPaiement
from domaine.Client import Client
from domaine.Collaborateur import Collaborateur
from domaine.Contrat import Contrat
from domaine.Devis import Devis
from domaine.Prestation import Prestation
from domaine.Facture import Facture
from domaine.Activite import Activite
from domaine.Paiement import Paiement


def _val(s):
    v = s.strip() if s else ""
    return None if v in ("", "None", "NULL") else v

def _int(s):
    v = _val(s)
    return int(v) if v else None

def _float(s):
    v = _val(s)
    return float(v) if v else None


def clean_database():
    DAOSession.clean_database()


def importation_clients_csv(filename="src/Interface_Tkinter/data/client/clients.csv"):
    dao = DAOClient.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            client = Client(
                id_client=_int(row["idClient"]),
                nom=_val(row["nom"]),
                prenom=_val(row["prenom"]),
                raison_sociale=_val(row["raisonSociale"]),
                adresse=_val(row["adressePostale"]),
                telephone=_val(row["telephone"]),
                courriel=_val(row["email"]),
                enum_status_client=_val(row["statut"]),
            )
            dao.insert_client(client)
            count += 1
    print(f"Clients importés : {count}")


def importation_collaborateurs_csv(filename="src/Interface_Tkinter/data/collaborateur/collaborateurs.csv"):
    dao = DAOCollaborateur.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            collaborateur = Collaborateur(
                id_collaborateur=_int(row["idCollaborateur"]),
                nom=_val(row["nom"]),
                prenom=_val(row["prenom"]),
                poste=_val(row["poste"]),
                telephone_pro=_val(row["telephonePro"]),
                numero_devis=_val(row["numeroDevis"]),
                id_utilisateur=None,
            )
            dao.insert_collaborateur(collaborateur)
            count += 1
    print(f"Collaborateurs importés : {count}")


def importation_contrats_csv(filename="src/Interface_Tkinter/data/contrat/contrats.csv"):
    dao = DAOContrat.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            contrat = Contrat(
                numero_contrat=_val(row["numeroContrat"]),
                date_debut=_val(row["dateDebut"]),
                duree=_val(row["duree"]),
                nb_productions_totales=_int(row["nbProductionsTotales"]),
                periodicite=_val(row["periodicite"]),
                montant_global=_float(row["montantGlobal"]),
                condition_paiements=_val(row["conditionsPaiement"]),
                id_client=_int(row["idClient"]),
            )
            dao.insert_contrat(contrat)
            count += 1
    print(f"Contrats importés : {count}")


def importation_devis_csv(filename="src/Interface_Tkinter/data/devis/devis.csv"):
    dao = DAODevis.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            devis = Devis(
                numero_devis=_val(row["numeroDevis"]),
                date_emission=_val(row["dateEmission"]),
                date_validite=_val(row["dateValidite"]),
                description_prestation=_val(row["descriptionPrestation"]),
                quantite_prevue=_int(row["quantitePrevue"]),
                details_couts=_val(row["detailsCouts"]),
                montant_total_estime=_float(row["montantTotalEstime"]),
                statut=_val(row["statut"]),
                date_acceptation=_val(row["dateAcceptation"]),
                id_client=_int(row["idClient"]),
                numero_contrat=_val(row["numeroContrat"]),
            )
            dao.insert_devis(devis)
            count += 1
    print(f"Devis importés : {count}")


def importation_prestations_csv(filename="src/Interface_Tkinter/data/prestation/prestations.csv"):
    dao = DAOPrestation.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            prestation = Prestation(
                id_prestation=_int(row["idPrestation"]),
                date_prevue=_val(row["datePrevue"]),
                date_effective=_val(row["dateEffective"]),
                lieu=_val(row["lieu"]),
                type_prestation=_val(row["type"]),
                nb_photos_prevues=_int(row["nbPhotosPrevues"]),
                nb_videos_prevues=_int(row["nbVideosPrevues"]),
                numero_contrat=_val(row["numeroContrat"]),
            )
            dao.insert_Prestation(prestation)
            count += 1
    print(f"Prestations importées : {count}")


def importation_factures_csv(filename="src/Interface_Tkinter/data/facture/factures.csv"):
    dao = DAOFacture.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            facture = Facture(
                numero_facture=_val(row["numeroFacture"]),
                date_emission=_val(row["dateEmission"]),
                montant_total=_float(row["montantTotal"]),
                etat=_val(row["etat"]),
                numero_contrat=_val(row["numeroContrat"]),
            )
            dao.insert_facture(facture)
            count += 1
    print(f"Factures importées : {count}")


def importation_activites_csv(filename="src/Interface_Tkinter/data/activite/activites.csv"):
    dao = DAOActivite.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            activite = Activite(
                id_activite=_int(row["idActivite"]),
                libelle_operationnel=_val(row["libelleOperationnel"]),
                date_prevues=_val(row["datePrevue"]),
                date_effective=_val(row["dateEffective"]),
                duree_estimee=_int(row["dureeEstimeeHeures"]),
                id_collaborateur=_int(row["idCollaborateur"]),
                statut=_val(row["statut"]),
                id_prestation=_int(row["idPrestation"]),
            )
            dao.insert_activite(activite)
            count += 1
    print(f"Activités importées : {count}")


def importation_paiements_csv(filename="src/Interface_Tkinter/data/paiement/paiements.csv"):
    dao = DAOPaiement.get_instance()
    count = 0
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            paiement = Paiement(
                id_paiement=_int(row["idPaiement"]),
                date=_val(row["datePaiement"]),
                montant=_float(row["montantPaye"]),
                numero_Facture=_val(row["numeroFacture"]),
            )
            dao.insert_paiement(paiement)
            count += 1
    print(f"Paiements importés : {count}")


def importation_combined_csv(dossier="src/Interface_Tkinter/data"):
    clean_database()
    importation_clients_csv(f"{dossier}/client/clients.csv")
    importation_contrats_csv(f"{dossier}/contrat/contrats.csv")
    importation_devis_csv(f"{dossier}/devis/devis.csv")
    importation_collaborateurs_csv(f"{dossier}/collaborateur/collaborateurs.csv")
    importation_prestations_csv(f"{dossier}/prestation/prestations.csv")
    importation_factures_csv(f"{dossier}/facture/factures.csv")
    importation_activites_csv(f"{dossier}/activite/activites.csv")
    importation_paiements_csv(f"{dossier}/paiement/paiements.csv")
