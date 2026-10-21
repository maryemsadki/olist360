from database import test_connection

try:
    database_name = test_connection()
    print("Connexion réussie !")
    print("Base de données :", database_name)

except Exception as error:
    print("Erreur de connexion :", error)