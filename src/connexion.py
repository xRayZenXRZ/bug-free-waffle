import mysql.connector
from mysql.connector import Error, errorcode, IntegrityError, InterfaceError

print(mysql.connector.__version__) # Version

config = {
    "host" : "localhost",
    "port" : 3306,
    "user" : "root",
    "password" : "", #Password à définir pour le root.
    "database" : "test_comart"
}

# if Connexion etablished :
try :

    connexion = mysql.connector.connect(**config)

    print(f'Connexion réussie à la base de données {config["database"]}')
    
    cursor = connexion.cursor()

    connexion.start_transaction()

# if Connexion is not etablished : 

except InterfaceError as err:
    print("Erreur de connexion : Impossible de se connecter au serveur MySQL.")

except IntegrityError as err:
    print(f"Erreur d'intégrité : {err}")
    connexion.rollback()

except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erreur d'authentification : Nom d'utilisateur ou mot de passe incorrect.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Erreur de base de données : La base de données spécifiée n'existe pas.")
    elif err.errno == errorcode.ER_PARSE_ERROR:
        print("Erreur de syntaxe dans la requête SQL.")
        connexion.rollback()
    elif err.errno == errorcode.ER_NO_SUCH_TABLE:
        print("Erreur : La table spécifiée n'existe pas.")
        connexion.rollback()
    elif err.errno == errorcode.ER_DUP_ENTRY:
        print("Erreur : Entrée déjà existante.")
        connexion.rollback()
    else:
        print(f"Erreur inattendue : {err}")
        connexion.rollback()

finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'connexion' in locals() and connexion is not None and connexion.is_connected():
        connexion.close()
        print("La connexion est fermée")

