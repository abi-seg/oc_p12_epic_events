import getpass
from cli.auth import run_login, run_logout, whoami
from models.base import Base, engine
from sqlalchemy import text
from cli.user_cli import run_create_user, list_all_users
from utils.jwt_manager import load_token
from cli.client_cli import run_create_client, list_clients, update_client, delete_client
from cli.contrat_cli import (
    run_create_contrat, run_list_contrats, run_update_contrat, run_delete_contrat,
    run_list_contrats_non_payes, run_list_contrats_non_signes)
from cli.evenement_cli import run_create_evenement, run_list_evenements, run_update_evenement

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
        payload = load_token()
        role = payload["role"] if payload else None

        print("\n ***** MENU PRINCIPAL *****")

        # --- Not logged in ---
        if not payload:
            print("1 - Se connecter")
            print("0 - Quitter")
            choice = input("Choisissez une option : ")

            if choice == "1":
                run_login()
            elif choice == "0":
                print("Au revoir!")
                break
            else:
                print("Option invalide.")
            continue  # restart loop

        # --- Logged in ---
        print(f"Connecté en tant que {payload['email']} (rôle : {role})")
        print("4 - Déconnexion")
        print("7 - Info utilisateur connecté (whoami)")

        # Lecture seule – tous les rôles
        print("6 - Voir les clients")
        print("11 - Voir les contrats")
        print("15 - Voir les événements")

        if role == "gestion":
            print("2 - Créer un utilisateur")
            print("3 - Voir tous les utilisateurs")
            print("5 - Créer un client")
            print("8 - Modifier un client")
            print("9 - Supprimer un client")

            print("10 - Créer un contrat")
            print("12 - Voir les contrats non signés")
            print("13 - Voir les contrats non entièrement payés")
            print("16 - Modifier un evenement")
            # plus tard : options événements (création, assignation support, etc.)

        elif role == "commercial":
            print("5 - Créer un client")
            print("8 - Modifier un client")

            print("10 - Créer un contrat")
            print("12 - Voir les contrats non signés")
            print("13 - Voir les contrats non entièrement payés")
            print("14 - Créer un événement")
            # plus tard : créer un événement pour un contrat signé

        elif role == "support":

            print("16 - Modifier un événement")

        choice = input("Choisissez une option : ")

        # --- Actions communes / existantes ---
        if choice == "2":
            run_create_user()           # déjà protégé par rôle à l’intérieur si tu veux
        elif choice == "3":
            list_all_users()
        elif choice == "4":
            run_logout()
        elif choice == "5":
            run_create_client()
        elif choice == "6":
            list_clients()
        elif choice == "7":
            whoami()
        elif choice == "8":
            update_client()
        elif choice == "9":
            delete_client()
        elif choice == "10":
            run_create_contrat()
        elif choice == "11":
            run_list_contrats()
        elif choice == "12":
            run_list_contrats_non_signes()
        elif choice == "13":
            run_list_contrats_non_payes()
        elif choice == "14":
            run_create_evenement()
        elif choice == "15":
            run_list_evenements()
        elif choice == "16":
            run_update_evenement()

        elif choice == "0":
            print("Au revoir!")
            break
        else:
            print("Option invalide.")


if __name__ == "__main__":
    main_menu()
