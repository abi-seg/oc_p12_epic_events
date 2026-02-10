from services.utilisateur_service import UtilisateurService
from models.base import Session


def run_login():
    """
    Runs the user loginflow in a command-line interface.
    This function prompts the user for their email and password,
    attempts authentication using the UtilisateurService, and
    displays a success or failure message based on the result.

    The database session is properly opened and closed during 
    the execution of the login process.

    """
    session = Session()
    service = UtilisateurService(session)
    email = input("Email: ")
    password = input("Mot de passe: ")
    user = service.login(email, password)

    if user:
        print(f"Connexion réussie! Bienvenue {user.nom} ({user.role})")
        session.close()
        return user  # return logged-in user
    else:
        print("échec de l'authentification")
        session.close()
        return None
