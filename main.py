from cli.auth import run_login
from models.base import Base, engine
from sqlalchemy import text
from cli.user_cli import run_create_user, list_all_users


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
        print("\n ***** MENU PRINCIPAL *****")
        print("1 - Créer un nouvel utilisateur")
        print("2 - Se connecter")
        print("3 - Voir tous les utilisateurs")
        print("4 - Quitter")

        choice = input("choissiez une option (1/2/3/4): ")
        if choice == "1":
            run_create_user()
        elif choice == "2":
            run_login()
        elif choice == "3":
            list_all_users()
        elif choice == "4":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main_menu()
