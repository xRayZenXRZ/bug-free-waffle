-- CRÉATION BASE DE DONNÉES : test_comart
DROP DATABASE IF EXISTS test_comart;
CREATE DATABASE IF NOT EXISTS test_comart;
USE test_comart;

CREATE TABLE Client (
    idClient        INT AUTO_INCREMENT PRIMARY KEY,
    typeClient      ENUM('PARTICULIER', 'ENTREPRISE') NOT NULL,
    nom             VARCHAR(100),
    prenom          VARCHAR(100),
    raisonSociale   VARCHAR(255),
    adressePostale  VARCHAR(255),
    telephone       VARCHAR(50),
    email           VARCHAR(255) UNIQUE NOT NULL,
    statut          ENUM('PROSPECT', 'CLIENT', 'ANCIEN') NOT NULL,

    CONSTRAINT check_particulier CHECK (
        (typeClient = 'PARTICULIER' AND nom IS NOT NULL AND prenom IS NOT NULL)
        OR
        (typeClient = 'ENTREPRISE'  AND raisonSociale IS NOT NULL)
    )
);

CREATE TABLE Utilisateur (
    idUtilisateur   INT AUTO_INCREMENT PRIMARY KEY,
    nom             VARCHAR(100)  NOT NULL,
    prenom          VARCHAR(100)  NOT NULL,
    email           VARCHAR(255)  UNIQUE NOT NULL,
    motDePasse      VARCHAR(255)  NOT NULL,
    role            ENUM('ADMIN', 'COLLABORATEUR') NOT NULL,
    statut          ENUM('ACTIF', 'INACTIF') DEFAULT 'ACTIF',
    dateCreation    DATETIME      DEFAULT CURRENT_TIMESTAMP,
    idCreateur      INT,
    FOREIGN KEY (idCreateur) REFERENCES Utilisateur(idUtilisateur)
);

CREATE TABLE Contrat (
    numeroContrat       VARCHAR(50) PRIMARY KEY,
    dateDebut           DATE,
    duree               VARCHAR(50),
    nbProductionsTotales INT,
    periodicite         ENUM('MENSUELLE', 'ANNUELLE', 'HEBDOMADAIRE'),
    montantGlobal       DECIMAL(10,2),
    conditionsPaiement  TEXT,
    idClient            INT,
    FOREIGN KEY (idClient) REFERENCES Client(idClient)
);

CREATE TABLE Devis (
    numeroDevis         VARCHAR(50) PRIMARY KEY,
    dateEmission        DATE,
    dateValidite        DATE,
    descriptionPrestation TEXT,
    quantitePrevue      INT,
    detailsCouts        TEXT,
    montantTotalEstime  DECIMAL(10,2),
    statut              ENUM('EN_ATTENTE', 'ACCEPTE', 'REFUSE', 'EXPIRE'),
    dateAcceptation     DATE,
    idClient            INT,
    numeroContrat       VARCHAR(50),
    FOREIGN KEY (idClient)       REFERENCES Client(idClient),
    FOREIGN KEY (numeroContrat)  REFERENCES Contrat(numeroContrat),

    CONSTRAINT chk_devis_dates CHECK (
        dateValidite IS NULL OR dateValidite >= dateEmission
    ),
    CONSTRAINT check_date_acceptation CHECK (
        (statut = 'ACCEPTE'    AND dateAcceptation IS NOT NULL)
        OR
        (statut IN ('REFUSE', 'EN_ATTENTE', 'EXPIRE') AND dateAcceptation IS NULL)
    )
);

CREATE TABLE Collaborateur (
    idCollaborateur INT AUTO_INCREMENT PRIMARY KEY,
    nom             VARCHAR(100) NOT NULL,
    prenom          VARCHAR(100) NOT NULL,
    poste           VARCHAR(255),
    telephonePro    VARCHAR(50),
    numeroDevis     VARCHAR(50),
    idUtilisateur   INT UNIQUE,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (numeroDevis)   REFERENCES Devis(numeroDevis)
);

CREATE TABLE Prestation (
    idPrestation    INT AUTO_INCREMENT PRIMARY KEY,
    datePrevue      DATETIME,
    dateEffective   DATETIME,
    lieu            VARCHAR(255),
    type            ENUM('COMM_REGULIERE', 'MARIAGE', 'EVENT_PRO', 'AUTRE'),
    nbPhotosPrevues INT,
    nbVideosPrevues INT,
    numeroContrat   VARCHAR(50),
    FOREIGN KEY (numeroContrat) REFERENCES Contrat(numeroContrat),
    CONSTRAINT date_check CHECK (dateEffective IS NULL OR dateEffective >= datePrevue)
);

CREATE TABLE Activite (
    idActivite          INT AUTO_INCREMENT PRIMARY KEY,
    libelleOperationnel VARCHAR(255),
    datePrevue DATETIME,
    dateEffective DATETIME,
    dureeEstimeeHeures INT,
    responsable VARCHAR(255),
    statut ENUM('PREVUE', 'EN_COURS', 'TERMINEE'),
    idPrestation INT,
    FOREIGN KEY(idPrestation) REFERENCES Prestation(idPrestation)
);