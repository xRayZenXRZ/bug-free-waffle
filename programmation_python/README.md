# Com'Art — Application de gestion de contenu

Application de gestion de la production et de la distribution de contenu pour l'agence **Com'Art** (Licence 2 MIASHS 2025-2026, Université de Lorraine).

---

## Prérequis

- Python 3.10+
- MySQL 8.0+
- Packages Python (voir `requirements.txt` à la racine) :
  - `mysql-connector-python`
  - `pandas`

Installation des dépendances :

```bash
pip install -r ../requirements.txt
```

---

## Configuration de la base de données

Ouvrir `dao/DAOSession.py` et renseigner les paramètres de connexion :

```python
HOST = "localhost"
LOGIN = "root"
MDP  = "votre_mot_de_passe"
DB   = "test_comart"
PORT = 3306
```

Créer la base et l'alimenter avec le script SQL fourni dans `../BD_Avancée/creation_alimentation.sql`.

---

## Lancement de l'application

Depuis le répertoire `programmation_python/` :

```bash
python main.py
```

L'écran de connexion s'affiche. Utiliser les identifiants d'un collaborateur existant en base.

Compte administrateur de test (inséré par le script SQL) :

| Email | Mot de passe |
|---|---|
| admin@comart.fr | Admin1234 |

---

## Architecture des modules

```
programmation_python/
├── main.py                      # Point d'entrée — initialise Tkinter et l'écran de connexion
├── comart_test.py               # Script de test rapide (ligne de commande)
│
├── domaine/                     # Classes métier (entités du domaine)
│   ├── Client.py
│   ├── Collaborateur.py
│   ├── Utilisateur.py
│   ├── Devis.py
│   ├── Contrat.py
│   ├── Prestation.py
│   ├── Activite.py
│   ├── Facture.py
│   ├── Paiement.py
│   └── Validators.py
│
├── dao/                         # Data Access Objects — toutes les requêtes SQL
│   ├── DAOSession.py            # Gestion unique de la connexion MySQL (singleton)
│   ├── DAOClient.py
│   ├── DAOCollaborateur.py
│   ├── DAOUtilisateur.py
│   ├── DAODevis.py
│   ├── DAOContrat.py
│   ├── DAOPrestation.py
│   ├── DAOActivite.py
│   ├── DAOFacture.py
│   └── DAOPaiement.py
│
├── Interface_Tkinter/           # Interface graphique (Tkinter)
│   ├── main_windows.py          # Fenêtre principale avec onglets (ttk.Notebook)
│   ├── Acceuil.py               # Écran de connexion
│   ├── gestion_client.py        # Onglet Clients
│   ├── gestion_devis.py         # Onglet Devis
│   ├── gestion_contrat.py       # Onglet Contrats
│   ├── gestion_prestations_activiter.py  # Onglet Prestations & Activités
│   ├── gestion_facture.py       # Onglet Facturation
│   ├── gestion_paiement.py      # Onglet Paiements
│   ├── gestion_utilisateur.py   # Gestion des comptes collaborateurs (admin)
│   ├── exportation.py           # Export CSV des données
│   ├── importation.py           # Import CSV en base de données
│   └── graphique.py             # Visualisations Matplotlib
│
└── data/                        # Fichiers de données de test (CSV)
    ├── client/
    ├── collaborateur/
    ├── contrat/
    ├── devis/
    ├── prestation/
    ├── activite/
    ├── facture/
    ├── paiement/
    └── combined/                # Vues jointes générées par exportation_combined_csv()
```

---

## Patron de conception

### Classes métier (`domaine/`)

Chaque classe métier suit le même patron :
- `__init__` : si la clé primaire est `None`, l'objet est **inséré en base** via le DAO associé ; sinon il est juste initialisé en mémoire.
- `charger(id)` : méthode statique qui **lit depuis la base** et reconstruit l'objet avec ses associations (ex. `Client.charger(3)` charge le client et ses devis).
- `supprimer(obj)` : méthode statique qui **supprime en base** avec vérification des dépendances.
- `ajouter_X / enlever_X` : gèrent les associations bidirectionnelles (ex. `contrat.ajouter_prestation(p)`).

### DAOs (`dao/`)

Chaque DAO implémente le pattern **Singleton** (`get_instance()`) et expose les opérations CRUD :
- `insert_*` → INSERT
- `find_*` → SELECT par clé primaire
- `select_*` → SELECT avec critères
- `update_*` → UPDATE
- `delete_*` → DELETE

**Aucune requête SQL n'apparaît en dehors des DAOs.**

---

## Données de test

Les fichiers CSV dans `data/` permettent de pré-remplir la base via le bouton **"Importer CSV"** de l'interface ou via le script `importation.py`.

Ordre d'importation requis (contraintes de clés étrangères) :

1. `client/clients.csv`
2. `contrat/contrats.csv`
3. `devis/devis.csv`
4. `collaborateur/collaborateurs.csv`
5. `prestation/prestations.csv`
6. `facture/factures.csv`
7. `activite/activites.csv`
8. `paiement/paiements.csv`

La fonction `importation_combined_csv()` effectue l'import dans le bon ordre après avoir nettoyé la base.

> Les comptes `Utilisateur` sont créés par le script SQL (`../BD_Avancée/creation_alimentation.sql`), pas par import CSV, car les mots de passe doivent être hashés côté base.
