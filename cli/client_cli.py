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
        print("Cette action est réservé aux utilisateurs commerciaux.")
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


def list_clients():
    """
    Displays a list of clients in the CLI based on the current user's role.

    This function:
        - Ensures a user is authenticated via the JWT payload.
        - Opens a database session and resolves the current utilisateur.
        - If the user has the 'gestion' role, all clients are listed.
        - If the user has the 'commercial' role, only clients assigned to 
          that commercial is listed.
        - For anyother role, access is denied
        - Prints a formatted list of clients or a message if none are found.
    """
    payload = load_token()
    if not payload:
        print("Veuillez vous connecter.")
        return
    session = Session()
    service = ClientService(session)
    user_service = UtilisateurService(session)
    user = user_service.repo.find_by_email(payload["email"])

    if payload["role"] == "gestion":
        clients = service.get_all_clients()  # lists all clients
    elif payload["role"] == "commercial":
        clients = service.get_clients_by_commercial_id(
            user.id)  # lists only clients hold by them
    else:
        print("Accès non autorisé pour votre role.")
        session.close()
        return
    if not clients:
        print("Aucun client trouvé.")
    else:
        print(" **** LISTE DES CLIENTS ****")
        for client in clients:
            commercial = client.commercial.nom if client.commercial else "Inconnu"
            print(
                f"- {client.nom_complet} | {client.email} | {client.entreprise} | Commercial : {commercial}")

    session.close()


def whoami():
    """
    Displays the information of the user who is actually connected.

    """
    payload = load_token()
    if not payload:
        print("Aucun utilisateur connecté.")
        return
    print(" **** UTILISATEUR CONNECTER ****")
    print(f" - Email : {payload['email']}")
    print(f" - Role : {payload['role']}")
