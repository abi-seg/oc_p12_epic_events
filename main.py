
from cli.auth import run_login, run_logout, whoami
from models.base import Base, engine
from sqlalchemy import text
from cli.user_cli import run_create_user, list_all_users, run_delete_user, run_update_user
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
        # Bloc commun
        print("4 - Déconnexion")

        # Clients & contrats : lecture pour tous
        print("7 - Voir les clients")
        print("11 - Voir les contrats")
        print("17 - Voir les événements")

        # -----Gestion------

        if role == "gestion":
            # Utilisateurs
            print("2 - Créer un utilisateur")
            print("3 - Voir tous les utilisateurs")
            print("19 - Modifier un utilisateur")
            print("20 - Supprimer un utilisateur")

            # Clients
            print("6 - Créer un client")
            print("8 - Modifier un client")
            print("9 - Supprimer un client")

            # Contrats

            print("10 - Créer un contrat")
            print("12 - Voir les contrats non signés")
            print("13 - Voir les contrats non entièrement payés")
            print("14 - Modifier un contrat")
            print("15 - Supprimer un contrat")

            # Evénements

            print("18 - Modifier un evenement")

            # ------- COMMERCIAL -------

        elif role == "commercial":
            # Clients

            print("6 - Créer un client")
            print("8 - Modifier un client")

            # Contrats

            print("10 - Créer un contrat")
            print("12 - Voir les contrats non signés")
            print("13 - Voir les contrats non entièrement payés")
            print("14 - Modifier un contrat")

            # Evénéménts
            print("16 - Créer un événémént")

        # ---- SUPPORT-----

        elif role == "support":

            # Evénéments

            print("18 - Modifier un événement")

        choice = input("Choisissez une option : ")

        # --- Actions  ---
        if choice == "2":
            run_create_user()           # déjà protégé par rôle à l’intérieur si tu veux
        elif choice == "3":
            list_all_users()
        elif choice == "4":
            run_logout()

        elif choice == "6":
            run_create_client()

        elif choice == "7":
            list_clients()
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
            run_update_contrat()
        elif choice == "15":
            run_delete_contrat()
        elif choice == "16":
            run_create_evenement()
        elif choice == "17":
            run_list_evenements()
        elif choice == "18":
            run_update_evenement()
        elif choice == "19":
            run_update_user()
        elif choice == "20":
            run_delete_user()
        elif choice == "0":
            print("Au revoir!")
            break
        else:
            print("Option invalide.")


if __name__ == "__main__":
    main_menu()
