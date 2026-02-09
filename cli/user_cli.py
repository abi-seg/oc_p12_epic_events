from services.utilisateur_service import UtilisateurService
from models.base import Session


def run_create_user():
    """
    Simple CLI to create a new utilisateur
    """
    session = Session()
    service = UtilisateurService(session)

    print("Créer un nouvel utilisateur")
    nom = input("Nom: ")
    email = input("Email: ")
    password = input("Mot de passe: ")
    role = input("Role (gestion, commercial, support): ")
    service.create_user(nom, email, password, role)
    print(f"L'utilisateur {nom} a été créé avec succès.")

    session.close()


def list_all_users():
    print("DEBUG: In list_all_users()")
    session = Session()
    service = UtilisateurService(session)

    users = service.list_users()
    print("\n Liste des utilisateurs: ")
    if not users:
        print("Aucun utilisateur trouvé.")
    for user in users:
        print(
            f"ID: {user.id}, Nom: {user.nom}, Email: {user.email}, Role: {user.role}")

    session.close()
