from services.utilisateur_service import UtilisateurService
from models.base import Session
from utils.jwt_manager import generate_token
import os
from getpass import getpass


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
    password = getpass("Mot de passe: ")  # secured password entry
    user = service.login(email, password)

    if user:
        print(f"Connexion réussie! Bienvenue {user.nom} ({user.role})")
        token = generate_token(user.email, user.role)
        # save token locally in .token file
        with open(".token", "w")as f:
            f.write(token)

        return user  # return logged-in user
    else:
        print("échec de l'authentification")
        user = None
        session.close()
        return user


def run_logout():
    """
     Log the user out by removing the saved authentication token.

    If the .token file exists, it is deleted so no further commands will
    be able to use the stored JWT. If the file does not exist, a message
    is printed indicating that no session token was found.
    """
    if os.path.exists(".token"):
        os.remove(".token")
        print("Déconnexion réussie.")
    else:
        print("Aucun token trouvé.")
