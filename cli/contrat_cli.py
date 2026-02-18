# cli/contrat_cli.py

from services.contrat_service import ContratService
from services.client_service import ClientService
from services.utilisateur_service import UtilisateurService
from models.base import Session
from utils.jwt_manager import load_token

# -----------------------
# Create a new contract
# -----------------------


def run_create_contrat():
    """
    Run the ineractive contract creation flow in the CLI.
    This function:
        - Verifies that the current user is authenticated.
        - Allows only 'gestion' and 'commercial' roles to create a contract.
        - Loads the logged-in user from the database using their email in the JWT.
        - Ask for the client ID and checks that the client exists.
        - If the user is 'commercial', checks that the client belongs to them.
        - Asks for the total amount and opeiton remaining amount.
        - Creats the contrat via ContratService.
    Access: Restricted to users with roles 'gestion' or 'commercial'.
    """

    payload = load_token()
    if not payload:
        print("Veuillez vous connecter.")
        return
    if payload["role"] not in ["commercial", "gestion"]:
        print("Accès interdit : seuls les utilisateurs GESTION ou COMMERCIAL "
              "peuvent créer un contrat")
        return

    session = Session()
    contrat_service = ContratService(session)
    client_service = ClientService(session)
    user_service = UtilisateurService(session)

    # Récuprer l'utilisateur connecté à partir de l'email dans le token
    user = user_service.repo.find_by_email(payload["email"])
    if not user:
        print("Utilisateur introuvable.")
        session.close()
        return
    print("***** CREATION D'UN CONTRAT *****")
    client_id_input = input("ID du client : ")
    try:
        client_id = int(client_id_input)
    except ValueError:
        print("ID client invalide.")
        session.close()
        return
    client = client_service.get_client_by_id(client_id)
    if not client:
        print("Client introuvable.")
        session.close()
        return
    # Règles d'accès :
    # - Si 'commercial' : il ne peut créer un contrat que pour SES clients
    # - Si 'gestion' : peut créer un contrat pour n'importe quel client
    if payload["role"] == "commercial" and client.commercial_id != user.id:
        print("Accès interdit : ce client n'est pas le vôtre.")
        session.close()
        return

    if payload["role"] == "gestion":
        commercial_id = client.commercial_id  # contrat lié au commercial du client
    else:  # commercial
        commercial_id = user.id

    montant_total_input = input("Montant total du contrat (€) : ")
    try:
        montant_total = float(montant_total_input)
    except ValueError:
        print("Montant invalide.")
        session.close()
        return

    montant_restant_input = input(
        "Montant restant à payer (laissez vide = même que le total) : "
    )
    if montant_restant_input:
        try:
            montant_restant = float(montant_restant_input)
        except ValueError:
            print("Montant invalide.")
            session.close()
            return
    else:
        montant_restant = montant_total

    # Création du contrat (non signé par défaut)
    contrat = contrat_service.create_contrat(
        client_id=client_id,
        commercial_id=commercial_id,
        montant_total=montant_total,
        montant_restant=montant_restant,
        statut=False
    )

    print(f"Contrat #{contrat.id} créé avec succès.")
    session.close()
