from datetime import datetime
from rich.table import Table
from rich.console import Console

from services.evenement_service import EvenementService
from services.contrat_service import ContratService
from services.utilisateur_service import UtilisateurService
from models.base import Session
from utils.jwt_manager import load_token

console = Console()


def run_create_evenement():
    """
    Run the interactive event creation flow in the CLI.

    Rules:
        - User must be authenticated.
        - Only 'commercial' can create an event.
        - The event must be linked to a signed contract belonging to this commercial.
        - Support is not assigned at creation time
    """
    payload = load_token()
    if not payload:
        print("Veuillez vous connecter.")
        return
    if payload["role"] != "commercial":
        print("Seuls les utilisateurs COMMERCIAL peuvent créer un événement.")
        return
    session = Session()
    evenement_service = EvenementService(session)
    contrat_service = ContratService(session)
    user_service = UtilisateurService(session)

    # Retrieve the logged-in user
    user = user_service.repo.find_by_email(payload["email"])
    if not user:
        print("Utilisateur introuvable.")
        session.close()
        return
    # Load contracts for this commercial and keep only signed ones
    contrats = contrat_service.get_contrats_by_commercial_id(user.id)
    contrats_signes = [c for c in contrats if c.statut]

    if not contrats_signes:
        print("Vous n'avez aucun contrat signé. Impossible de créer un événement.")
        session.close()
        return
    # Display signed contracts with rich
    table = Table(title="Contrats signés disponibles pour créer un événémént")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Client", style="magenta")
    table.add_column("Total (£)", justify="right", style="green")
    table.add_column("Restant (£)", justify="right", style="yellow")
    table.add_column("Date", style="white")

    for c in contrats_signes:
        client_name = c.client.nom_complet if c.client else "Inconnu"
        date_str = c.date_creation.strftime(
            "%Y-%m-%d") if c.date_creation else "N/A"
        table.add_row(
            str(c.id),
            client_name,
            f"{float(c.montant_total):.2f}",
            f"{float(c.montant_restant):.2f}",
            date_str,

        )
    console.print(table)

    contrat_id_input = input("ID du contrat pour l'événement : ")
    try:
        contrat_id = int(contrat_id_input)
    except ValueError:
        print("ID de contrat invalide.")
        session.close()
        return

    contrat = contrat_service.get_contrat_by_id(contrat_id)
    if not contrat or contrat not in contrats_signes:
        print("Contrat invalide ou non signé.")
        session.close()
        return

    client = contrat.client
    if not client:
        print("Client associé au contrat introuvable.")
        session.close()
        return

    # Pre-fill client info from the related Client entity
    nom_client = client.nom_complet
    contact_client = f"{client.email} / {client.telephone}"

    print("**** Création d'un événement ****")
    date_debut_str = input("Date de début (AAAA-MM-JJ HH:MM) : ")
    date_fin_str = input("Date de fin (AAAA-MM-JJ HH:MM) : ")
    lieu = input("Lieu : ")
    participants_input = input("Nombre de participants : ")
    notes = input("Notes (optionnel) : ")

    try:
        date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d %H:%M")
        date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Format de date/heure invalide. Utilisez AAAA-MM-JJ HH:MM.")
        session.close()
        return

    try:
        participants = int(participants_input)
    except ValueError:
        print("Nombre de participants invalide.")
        session.close()
        return

    evenement = evenement_service.create_evenement(
        contrat_id=contrat.id,
        nom_client=nom_client,
        contact_client=contact_client,
        date_debut=date_debut,
        date_fin=date_fin,
        lieu=lieu,
        participants=participants,
        notes=notes or None,
        support_id=None,  # assigned later by gestion
    )

    print(
        f"Événement #{evenement.id} créé avec succès pour le client {nom_client}.")
    session.close()
