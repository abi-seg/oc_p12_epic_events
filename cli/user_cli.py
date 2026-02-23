from services.utilisateur_service import UtilisateurService
from models.base import Session
from utils.jwt_manager import load_token


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
    payload = load_token()
    if not payload or payload['role'] != 'gestion':
        print("Accès refusé. GESTION Uniquement.")
        return

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
# cli/user_cli.py


def run_update_user():
    """
    Interactive update of a user (utilisateur) in the CLI.

    - Only 'gestion' can update users.
    - Allows updating name, email, role, password.
    """
    payload = load_token()
    if not payload or payload["role"] != "gestion":
        print("Seul le rôle GESTION peut modifier un utilisateur.")
        return

    session = Session()
    service = UtilisateurService(session)

    # List all users
    users = service.list_users()
    if not users:
        print("Aucun utilisateur trouvé.")
        session.close()
        return

    print("**** LISTE DES UTILISATEURS ****")
    print(f"{'ID':<4} | {'Nom':<15} | {'Email':<30} | {'Rôle':<10}")
    print("-" * 65)
    for u in users:
        print(f"{u.id:<4} | {u.nom:<15} | {u.email:<30} | {u.role:<10}")

    user_id_input = input("ID de l'utilisateur à modifier : ")
    try:
        user_id = int(user_id_input)
    except ValueError:
        print("ID invalide.")
        session.close()
        return

    utilisateur = service.get_user_by_id(user_id)
    if not utilisateur:
        print("Utilisateur introuvable.")
        session.close()
        return

    print("Laissez vide pour ne pas modifier un champ.")
    new_nom = input(f"Nouveau nom ({utilisateur.nom}) : ")
    new_email = input(f"Nouvel email ({utilisateur.email}) : ")
    new_role = input(
        f"Nouveau rôle ({utilisateur.role}) [gestion/commercial/support] : ")
    new_pwd = input("Nouveau mot de passe (laisser vide = ne pas changer) : ")

    # Validate role if changed
    if new_role and new_role not in ("gestion", "commercial", "support"):
        print("Rôle invalide.")
        session.close()
        return

    # Prepare values; None means "no change"
    nom_val = new_nom if new_nom else None
    email_val = new_email if new_email else None
    role_val = new_role if new_role else None
    pwd_val = new_pwd if new_pwd else None

    if not any([nom_val, email_val, role_val, pwd_val]):
        print("Aucune modification appliquée.")
        session.close()
        return

    service.update_user(
        utilisateur,
        nom=nom_val,
        email=email_val,
        role=role_val,
        mot_de_passe=pwd_val,
    )
    print("Utilisateur mis à jour avec succès.")
    session.close()


def run_delete_user():
    """
    Interactive deletion of a user.

    - Only 'gestion' can delete users.
    """
    payload = load_token()
    if not payload or payload["role"] != "gestion":
        print("Seul le rôle GESTION peut supprimer un utilisateur.")
        return

    session = Session()
    service = UtilisateurService(session)

    users = service.list_users()
    if not users:
        print("Aucun utilisateur trouvé.")
        session.close()
        return

    print("**** LISTE DES UTILISATEURS ****")
    print(f"{'ID':<4} | {'Nom':<15} | {'Email':<30} | {'Rôle':<10}")
    print("-" * 65)
    for u in users:
        print(f"{u.id:<4} | {u.nom:<15} | {u.email:<30} | {u.role:<10}")

    user_id_input = input("ID de l'utilisateur à supprimer : ")
    try:
        user_id = int(user_id_input)
    except ValueError:
        print("ID invalide.")
        session.close()
        return

    utilisateur = service.get_user_by_id(user_id)
    if not utilisateur:
        print("Utilisateur introuvable.")
        session.close()
        return

    # Optional: prevent deleting yourself
    if utilisateur.email == payload["email"]:
        print("Vous ne pouvez pas supprimer votre propre compte.")
        session.close()
        return

    confirm = input(
        f"Supprimer l'utilisateur {utilisateur.nom} ({utilisateur.email}) ? (o/n) : ")
    if confirm.lower() == "o":
        service.delete_user(utilisateur)
        print("Utilisateur supprimé.")
    else:
        print("Suppression annulée.")

    session.close()
