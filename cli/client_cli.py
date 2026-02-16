from services.client_service import ClientService
from services.utilisateur_service import UtilisateurService
from models.base import Session
from utils.jwt_manager import load_token


def run_create_client():
    """
    Run the interactive client creation flow in the CLI.
    This function:
        - Validates that the current user is authenticated as a commercial
          using the JWT payload.
        - Prompts the user for client information via the command line.
        - Uses the ClientService to create and persist a new Client
          associated with the logged-in commercial.
        - Displays a success or error message accordingly.
    Access to this action is restricted to users with the 'commercial' role.

    """
    payload = load_token()
    if not payload or payload["role"] != "commercial":
        print("Access réservé aux utilisateurs commerciaux.")
        return
    session = Session()
    service = ClientService(session)
    print("**** Création d'un client **** ")
    nom = input("Nom complet : ")
    email = input("Email : ")
    phone = input("Téléphone : ")
    entreprise = input("Entreprise : ")

    # Get current commercial user's ID
    user_service = UtilisateurService(session)
    user = user_service.repo.find_by_email(payload["email"])

    if user:
        client = service.create_client(nom, email, phone, entreprise, user.id)
        print(f"Client '{client.nom_complet}' crée avec success. ")

    else:
        print("Utilisateur non trouvé.")

    session.close()
