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


def run_list_contrats():
    """
    Display a list of contracts in the CLI based on the current user's role.

    This function:
      - Ensures a user is authenticated via the JWT payload.
      - Opens a database session and builds the ContratService.
      - If the user has the 'gestion' role, all contracts are listed.
      - If the user has the 'commercial' role, only contracts linked to
        that commercial are listed.
      - For other roles, access is denied (you can change this later to
        allow read-only access if desired).
      - Prints a formatted table of contracts including client and
        commercial names.

    Access
    ------
    'gestion'  : all contracts
    'commercial' : own contracts
    others : denied (for now)
    """
    payload = load_token()
    if not payload:
        print("Veuillez vous connecter.")
        return

    session = Session()
    contrat_service = ContratService(session)
    user_service = UtilisateurService(session)

    # Retrieve the logged-in user from the database
    user = user_service.repo.find_by_email(payload["email"])
    if not user:
        print("Utilisateur introuvable.")
        session.close()
        return

    role = payload["role"]

    if role == "gestion":
        contrats = contrat_service.get_all_contrats()
    elif role == "commercial":
        contrats = contrat_service.get_contrats_by_commercial_id(user.id)
    else:
        print("Accès non autorisé pour votre rôle.")
        session.close()
        return

    if not contrats:
        print("Aucun contrat trouvé.")
        session.close()
        return

    print(" **** LISTE DES CONTRATS ****")
    print(
        f"{'ID':<4} | {'Client':<25} | {'Commercial':<15} | "
        f"{'Total (€)':<10} | {'Restant (€)':<12} | {'Date':<12} | {'Statut':<8}"
    )
    print("-" * 100)

    for c in contrats:
        client_name = c.client.nom_complet if c.client else "Inconnu"
        commercial_name = c.commercial.nom if c.commercial else "Inconnu"
        statut_label = "Signé" if c.statut else "Non signé"
        date_str = c.date_creation.strftime(
            "%Y-%m-%d") if c.date_creation else "N/A"

        print(
            f"{c.id:<4} | {client_name:<25} | {commercial_name:<15} | "
            f"{float(c.montant_total):<10.2f} | {float(c.montant_restant):<12.2f} | "
            f"{date_str:<12} | {statut_label:<8}"
        )

    session.close()


def run_update_contrat():
    """
    Run the interactive contract update flow in the CLI.

    This function:
      - Verifies that the current user is authenticated.
      - Allows 'gestion' to modify any contract.
      - Allows 'commercial' to modify only contracts linked to their own clients.
      - Lists the relevant contracts for selection.
      - Prompts the user for new values (total, remaining, statut),
        leaving fields empty to keep current values.
      - Applies the updates via ContratService.

    Access
    ------
    'gestion'    : can modify all contracts
    'commercial' : can modify only their own contracts
    others       : denied
    """
    payload = load_token()
    if not payload:
        print("Veuillez vous connecter.")
        return

    if payload["role"] not in ("gestion", "commercial"):
        print("Accès non autorisé à la modification de contrat.")
        return

    session = Session()
    contrat_service = ContratService(session)
    user_service = UtilisateurService(session)

    user = user_service.repo.find_by_email(payload["email"])
    if not user:
        print("Utilisateur introuvable.")
        session.close()
        return

    role = payload["role"]

    # Determine which contracts the user can see
    if role == "gestion":
        contrats = contrat_service.get_all_contrats()
    else:  # commercial
        contrats = contrat_service.get_contrats_by_commercial_id(user.id)

    if not contrats:
        print("Aucun contrat disponible pour modification.")
        session.close()
        return

    print("\n Vos contrats :")
    for c in contrats:
        client_name = c.client.nom_complet if c.client else "Inconnu"
        statut_label = "Signé" if c.statut else "Non signé"
        print(
            f"ID: {c.id} | Client: {client_name} | Total: {float(c.montant_total):.2f}€ | "
            f"Restant: {float(c.montant_restant):.2f}€ | Statut: {statut_label}"
        )

    contrat_id_input = input("Entrez l’ID du contrat à modifier : ")

    try:
        contrat_id = int(contrat_id_input)
    except ValueError:
        print("ID de contrat invalide.")
        session.close()
        return

    contrat = contrat_service.get_contrat_by_id(contrat_id)
    if not contrat:
        print("Contrat introuvable.")
        session.close()
        return

    # Security: commercial can only modify their own contracts
    if role == "commercial" and contrat.commercial_id != user.id:
        print("Vous ne pouvez modifier que vos propres contrats.")
        session.close()
        return

    print("Laissez vide pour ne pas modifier un champ.")
    new_total_input = input(
        f"Nouveau montant total ({float(contrat.montant_total):.2f}) : ")
    new_rest_input = input(
        f"Nouveau montant restant ({float(contrat.montant_restant):.2f}) : ")
    new_statut_input = input(
        f"Le contrat est-il signé ? (o/n, laisser vide pour ne pas modifier) [Actuel: "
        f"{'signé' if contrat.statut else 'non signé'}] : "
    )

    updates = {}

    if new_total_input:
        try:
            updates["montant_total"] = float(new_total_input)
        except ValueError:
            print("Montant total invalide.")
            session.close()
            return

    if new_rest_input:
        try:
            updates["montant_restant"] = float(new_rest_input)
        except ValueError:
            print("Montant restant invalide.")
            session.close()
            return

    if new_statut_input.lower() == "o":
        updates["statut"] = True
    elif new_statut_input.lower() == "n":
        updates["statut"] = False
    # if empty → no change

    if not updates:
        print("Aucune modification appliquée.")
        session.close()
        return

    contrat_service.update_contrat(contrat, **updates)
    print("Contrat mis à jour avec succès.")
    session.close()


def run_delete_contrat():
    """
    Run the interactive contract deletion flow in the CLI.

    This function:
      - Verifies that the current user is authenticated and has the
        'gestion' role.
      - Prompts for the ID of the contract to delete.
      - Loads the corresponding Contrat entity.
      - Asks for confirmation before deletion.
      - Delegates removal to ContratService.

    Access
    ------
    Restricted to users with the 'gestion' role.
    """
    payload = load_token()
    if not payload or payload["role"] != "gestion":
        print("Seul le rôle GESTION peut supprimer un contrat.")
        return

    session = Session()
    contrat_service = ContratService(session)

    contrat_id_input = input("ID du contrat à supprimer : ")
    try:
        contrat_id = int(contrat_id_input)
    except ValueError:
        print("ID de contrat invalide.")
        session.close()
        return

    contrat = contrat_service.get_contrat_by_id(contrat_id)
    if not contrat:
        print("Contrat non trouvé.")
        session.close()
        return

    client_name = contrat.client.nom_complet if contrat.client else "Inconnu"
    confirm = input(
        f"Supprimer le contrat #{contrat.id} pour le client '{client_name}' ? (o/n): "
    )

    if confirm.lower() == "o":
        contrat_service.delete_contrat(contrat)
        print("Contrat supprimé.")
    else:
        print("Suppression annulée.")

    session.close()
