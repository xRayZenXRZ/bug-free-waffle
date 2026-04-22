--- CREATION BASE DE DONNEES
DROP DATABASE IF EXISTS test_comart;
CREATE DATABASE IF NOT EXISTS test_comart;

USE test_comart;

--    CLIENT
CREATE TABLE Client (
    idClient INT AUTO_INCREMENT PRIMARY KEY,
    typeClient ENUM('PARTICULIER', 'ENTREPRISE') NOT NULL,
    nom VARCHAR(100),              -- NULL si entreprise
    prenom VARCHAR(100),           -- NULL si entreprise
    raisonSociale VARCHAR(255),    -- NULL si particulier
    adressePostale VARCHAR(255),
    telephone VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    statut ENUM('PROSPECT', 'CLIENT', 'ANCIEN') NOT NULL,

    -- Contraintes de cohérence selon le type
    CONSTRAINT check_particulier CHECK (
        (typeClient = 'PARTICULIER' AND nom IS NOT NULL AND prenom IS NOT NULL)
        OR
        (typeClient = 'ENTREPRISE' AND raisonSociale IS NOT NULL)
    )
);

--          CONTRAT
CREATE TABLE Contrat (
    numeroContrat VARCHAR(50) PRIMARY KEY,
    dateDebut DATE,
    duree VARCHAR(50),
    nbProductionsTotales INT,
    periodicite ENUM('MENSUELLE', 'ANNUELLE','HEBDOMADAIRE'),
    montantGlobal DECIMAL(10,2),
    conditionsPaiement TEXT,
    idClient int, 
    FOREIGN KEY (idClient) REFERENCES Client(idClient)
);

--           DEVIS
CREATE TABLE Devis (
    numeroDevis VARCHAR(50) PRIMARY KEY,
    dateEmission DATE,
    dateValidite DATE,
    descriptionPrestation TEXT,
    quantitePrevue INT,
    detailsCouts TEXT,
    montantTotalEstime DECIMAL(10,2),
    statut ENUM('EN_ATTENTE', 'ACCEPTE', 'REFUSE', 'EXPIRE'),
    dateAcceptation date,
    idClient INT REFERENCES Client(idClient),
    numeroContrat VARCHAR(50), 
    FOREIGN KEY(numeroContrat) REFERENCES Contrat(numeroContrat),
    CONSTRAINT chk_devis_dates CHECK (dateValidite IS NULL OR dateValidite >= dateEmission),
    
    -- Contraintes de cohérence selon le statut du devis
    CONSTRAINT check_date_acceptation CHECK (
        (statut = 'ACCEPTE' AND dateAcceptation IS NOT NULL)
        OR
        (statut = 'REFUSE' AND dateAcceptation IS  NULL)
        OR
        (statut = 'EN_ATTENTE' AND dateAcceptation IS  NULL)
        OR
        (statut = 'EXPIRE' AND dateAcceptation IS  NULL)
    )
    );

--          FACTURE
CREATE TABLE Facture (
    numeroFacture VARCHAR(50) PRIMARY KEY,
    dateEmission DATE,
    montantTotal DECIMAL(10,2),
    etat ENUM('EN_ATTENTE', 'PAYEE', 'PARTIELLEMENT_PAYEE'),
    numeroContrat VARCHAR(50), 
    FOREIGN KEY(numeroContrat) REFERENCES Contrat(numeroContrat)
);

--          PAIEMENT
CREATE TABLE Paiement (
  idPaiement INT AUTO_INCREMENT PRIMARY KEY,
  datePaiement DATE NOT NULL,
  montantPaye NUMERIC(14,2) NOT NULL CHECK (montantPaye >= 0),
  numeroFacture VARCHAR(50) NOT NULL,
   FOREIGN KEY(numeroFacture) REFERENCES Facture(numeroFacture)

);

--        PRESTATION
CREATE TABLE Prestation (
    idPrestation INT AUTO_INCREMENT PRIMARY KEY,
    datePrevue DATETIME,
    dateEffective DATETIME,
    lieu VARCHAR(255),
    type ENUM('COMM_REGULIERE', 'MARIAGE', 'EVENT_PRO', 'AUTRE'),
    nbPhotosPrevues INT,
    nbVideosPrevues INT,
    numeroContrat VARCHAR(50),
    FOREIGN KEY(numeroContrat) REFERENCES Contrat(numeroContrat),
    CONSTRAINT date_check CHECK (dateEffective IS NULL OR dateEffective >= datePrevue)
);

--         ACTIVITÉ
CREATE TABLE Activite (
    idActivite INT AUTO_INCREMENT PRIMARY KEY,
    libelleOperationnel VARCHAR(255),
    datePrevue DATETIME,
    dateEffective DATETIME,
    dureeEstimeeHeures INT,
    responsable VARCHAR(255),
    statut ENUM('PREVUE', 'EN_COURS', 'TERMINEE'),
    idPrestation INT,
    FOREIGN KEY(idPrestation) REFERENCES Prestation(idPrestation)
);

-- UTILISATEUR (Collaborateurs et Admins)
CREATE TABLE Utilisateur (
    idUtilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    motDePasse VARCHAR(255) NOT NULL,  -- À hasher en production !
    role ENUM('ADMIN', 'COLLABORATEUR') NOT NULL,
    statut ENUM('ACTIF', 'INACTIF') DEFAULT 'ACTIF',
    dateCreation DATETIME DEFAULT CURRENT_TIMESTAMP,
    idCreateur INT,  -- Quel admin a créé ce compte
    FOREIGN KEY(idCreateur) REFERENCES Utilisateur(idUtilisateur)
);

-- Insérer un admin par défaut
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, role) 
VALUES ('Admin', 'Principal', 'root@gmail.com', 'root', 'ADMIN');
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, statut , role) 
VALUES ('Admin', 'Principal', 'root@gmail.com', 'root', 'INACTIF', 'ADMIN');