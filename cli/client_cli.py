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
        print(
            f"{'ID':<4} | {'Nom complet':<20} | {'Email':<30} | {'Entreprise':<25} | Commercial")
        print("-" * 110)

    for client in clients:
        commercial_name = client.commercial.nom if client.commercial else "Non assigné"
        print(f"{client.id:<4} | {client.nom_complet:<20} | {client.email:<30} | {client.entreprise:<25} | {commercial_name}")
    session.close()


def update_client():
    """
    Run the interactive client update flow in the CLI for commercial users.

    This function:
      - Verifies that the current user is authenticated and has the
        'commercial' role via the JWT payload.
      - Loads the logged-in commercial from the database and retrieves
        only the clients assigned to that user.
      - Displays the list of these clients and prompts for the ID of
        the client to update.
      - Ensures the selected client exists and belongs to the current
        commercial before allowing any modification.
      - Prompts for new values for each field (name, email, phone,
        company), allowing the user to leave fields empty to keep the
        existing values.
      - Applies the requested changes through the ClientService and
        confirms the update in the CLI.

    Access
    ------
    Restricted to users with the 'commercial' role.
    """
    payload = load_token()
    if not payload:
        print("Veuillez vous connecter.")
        return

    session = Session()
    user_service = UtilisateurService(session)
    user = user_service.repo.find_by_email(payload["email"])
    client_service = ClientService(session)

    #  Gestion sees all the clients, commercial sees only theirs
    if payload['role'] == 'gestion':
        clients = client_service.get_all_clients()
    elif payload['role'] == 'commercial':
        clients = client_service.get_clients_by_commercial_id(user.id)
    else:
        print("Accès non autorisé à la modification de client.")
    # show clients to select from
    if not clients:
        print(" Vous n’avez aucun client.")
        session.close()
        return

    print("\n Vos clients :")
    for client in clients:
        print(
            f"ID: {client.id} | Nom: {client.nom_complet} | Entreprise: {client.entreprise}")

    client_id = input("Entrez l’ID du client à modifier : ")
    client = client_service.get_client_by_id(client_id)

    if not client:
        print(" Client introuvable.")
        session.close()
        return
   # check if commercial owns this client

    if payload["role"] == "commercial" and client.commercial_id != user.id:
        print(" Vous ne pouvez modifier que vos propres clients.")
        session.close()
        return

    # Input modifications
    print("Laissez vide pour ne pas modifier un champ.")
    new_nom = input(f"Nouveau nom ({client.nom_complet}): ")
    new_email = input(f"Nouveau email ({client.email}): ")
    new_phone = input(f"Nouveau téléphone ({client.telephone}): ")
    new_entreprise = input(f"Nouveau entreprise ({client.entreprise}): ")

    updates = {}
    if new_nom:
        updates["nom_complet"] = new_nom
    if new_email:
        updates["email"] = new_email
    if new_phone:
        updates["telephone"] = new_phone
    if new_entreprise:
        updates["entreprise"] = new_entreprise

    client_service.update_client(client, **updates)
    print("Client mis à jour avec succès.")

    session.close()


def delete_client():
    """
    Run the interactive client deletion flow in the CLI for admin users.

    This function:
      - Verifies that the current user is authenticated and has the
        'gestion' role using the JWT payload.
      - Opens a database session and resolves the ClientService.
      - Prompts for the ID of the client to delete and attempts to load
        the corresponding Client entity.
      - If the client exists, asks for a confirmation before deletion.
      - Delegates the actual removal to the ClientService and reports
        the result in the CLI.

    Access
    ------
    Restricted to users with the 'gestion' role.
    """
    payload = load_token()
    if not payload or payload["role"] != "gestion":
        print("Seul le gestion peut supprimer un client.")
        return

    session = Session()
    service = ClientService(session)

    client_id = input("ID du client à supprimer : ")
    client = service.get_client_by_id(client_id)

    if not client:
        print(" Client non trouvé.")
    else:
        confirm = input(f"Supprimer {client.nom_complet} ? (o/n): ")
        if confirm.lower() == 'o':
            service.delete_client(client)
            print(" Client supprimé.")
    session.close()
