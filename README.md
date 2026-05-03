# bug-free-waffle

Pour sauvegarder : git add . && git commit -m "commentaires" && git push

Keyword :

- Created_inc = Creation incomplete(à completer plus tard)

Pour récuperer : git pull

##  Avancer de lancer le projet
pip install -r requirements.txt
## Project Structure

```
src
│
├── DAO : Pour tous les methodes DAO, verifier leur fonctionnement et modifier en consequence (methode : insert fonctionne, donc pas à le faire )
│   ├── DAOActivite 
│   ├── DAOClient
│   ├── DAOCompteUtilisateur
│   ├── DAOContrat
│   ├── DAODevis
│   ├── DAOFacture
│   ├── DAOPaiement
│   ├── DAOPrestation
│   └── DAOSession
│
├── domaine : Pour tous les methodes setter et dans __init__ faire les vérifications de type à faire (exemple finis : Client)
│   ├── Activite 
│   ├── Client 
│   ├── CompteUtilisateur
│   ├── Contrat
│   ├── Devis
│   ├── Facture
│   ├── Paiement
│   └── Prestation
│   
├── Interface_Tkinter
│   ├── Acceuil : acceuil avec les onglet encore à faire
│   └── main : les verifications sont très fragiles donc à modifier.
│
├── comart_test : faire ici pour les test d'insertion ou de suppressions (pensez bien à reLancer test.sql pour vérifier si ca fonctionnne à chaque fois)
└── connexion
```
