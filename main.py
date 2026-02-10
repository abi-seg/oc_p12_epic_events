from cli.auth import run_login, run_logout
from models.base import Base, engine
from sqlalchemy import text
from cli.user_cli import run_create_user, list_all_users
from utils.jwt_manager import load_token


# Placeholder - no models yet, we just test the connection
Base.metadata.create_all(engine)

print("Connexion réussie à la base de données MySQL.")

# To get the name of the DB
with engine.connect() as connection:
    result = connection.execute(text("SELECT DATABASE();"))
    db_name = result.scalar()
    print(f"Nom de la base de données : {db_name}")


def main_menu():

    while True:
        payload = load_token  # check if user is authenticated
        print("\n ***** MENU PRINCIPAL *****")
        print("1 - Se connecter")
        if payload:
            print("2 - Créer un utilisateur")  # Gestion only
            print("3 - Voir tous les utilisateurs")  # Gestion only
            print("4 - Déconnexion")
        print("0 - Quitter")

        choice = input("choissiez une option : ")
        if choice == "1":
            logged_user = run_login()  # store logged-in user
        elif choice == "2":
            if payload and payload['role'] == "gestion":
                run_create_user()
            else:
                print("Access interdit. GESTION Uniquement.")
        elif choice == "3":
            if payload and payload['role'] == "gestion":
                list_all_users()
            else:
                print("Access interdit. GESTION Uniquement.")
        elif choice == "4":
            run_logout

        elif choice == "0":
            print("Au revoir!")
            break
        else:
            print("Option invalide.")


if __name__ == "__main__":
    main_menu()
