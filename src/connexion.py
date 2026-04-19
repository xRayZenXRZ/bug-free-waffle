"""import mysql.connector
from mysql.connector import Error, errorcode, IntegrityError, InterfaceError

#print(mysql.connector.__version__) # Version

config = {
    "host" : "localhost",
    "port" : 0000,
    "user" : "root",
    "password" : None, #Password à définir pour le root.
    "database" : "todo"
}

# if Connexion etablished :
try :

    config = mysql.connector.connect(**config)

    print(f"Connexion réussie à la base de données {config["database"]}")
    
    cursor = config.cursor()

    config.start_transaction()


# fi Connexion is not etablished : 

except InterfaceError as err:
    print("Erreur de connexion : Impossible de se connecter au serveur MySQL.")

except IntegrityError as err:
    print(f"Erreur d'intégrité : {err}")
    config.rollback()

except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erreur d'authentification : Nom d'utilisateur ou mot de passe incorrect.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Erreur de base de données : La base de données spécifiée n'existe pas.")
    elif err.errno == errorcode.ER_PARSE_ERROR:
        print("Erreur de syntaxe dans la requête SQL.")
        config.rollback()
    elif err.errno == errorcode.ER_NO_SUCH_TABLE:
        print("Erreur : La table spécifiée n'existe pas.")
        config.rollback()
    elif err.errno == errorcode.ER_DUP_ENTRY:
        print("Erreur : Entrée déjà existante.")
        config.rollback()
    else:
        print(f"Erreur inattendue : {err}")
        config.rollback()

finally:
    if 'cursor' in locals() and cursor is not None:
        config.close()
    if 'config' in locals() and config is not None and config.is_connected():
        config.close()
        print("La connexion est fermée")"""