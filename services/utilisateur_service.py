from models.utilisateur import Utilisateur
from utils.security import hash_password, verify_password
from repositories.utilisateur_repository import UtilisateurRepository
import sentry_sdk


class UtilisateurService:
    """
    Service layer responsible for user-related business logic.

    This class handles user creation and authentication while delegating
    presistance operations to the UtilisateurRepository.

    """

    def __init__(self, session):
        """
        Intializes the service with a database session.

        :param session: SQLALchemy session used to access the repository.

        """
        self.repo = UtilisateurRepository(session)

    def create_user(self, nom, email, password, role):
        """
        Creates and save the new utilisateur.
        The password is securely hashed before being stored.

        :param nom: User's name.
        :type nom:str
        :param email: user's email address
        :type email: str
        :param password: plain text password
        :type role : str
        :return: The newly created Utilisateur
        :rtype: Utilisateur

        """
        hashed = hash_password(password)
        utilisateur = Utilisateur(
            nom=nom, email=email, mot_de_passe=hashed, role=role)
        self.repo.save(utilisateur)

    # Journalisation Sentry
        sentry_sdk.capture_message(
            f"[USER_CREATED] id={utilisateur.id}, email={utilisateur.email}, role={utilisateur.role}",
            level="info"
        )
        return utilisateur

    def login(self, email, password):
        """
        Authenticates a user using email and password.
        The provided password is verified against the stored hashed password.

        :param email: User's email address.
        :type email: str
        :param password: plain text password
        :type password: str
        :return: The authenticated Utilisateur if credentials are valid, otherwise None.

        """
        user = self.repo.find_by_email(email)
        if user and verify_password(password, user.mot_de_passe):
            return user
        return None

    def list_users(self):
        """
        Get all users via repository
        :return: list of utilisateurs

        """
        return self.repo.get_all()

    def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by its identifier.
        """
        return self.repo.get_by_id(user_id)

    def update_user(self, utilisateur, nom=None, email=None,
                    role=None, mot_de_passe=None):
        """
        Update an existing user with the given field values.

        mot_de_passe, if provided, will be re-hashed.
        """
        old_data = {
            "nom": utilisateur.nom,
            "email": utilisateur.email,
            "role": utilisateur.role,
        }
        if nom is not None:
            utilisateur.nom = nom
        if email is not None:
            utilisateur.email = email
        if role is not None:
            utilisateur.role = role
        if mot_de_passe is not None:
            utilisateur.mot_de_passe = hash_password(mot_de_passe)

        self.repo.update(utilisateur)
        # Sentry Journalisation
        sentry_sdk.capture_message(
            f"[USER_UPDATED] id={utilisateur.id},"
            f"old={old_data},"
            f"new={{'nom': '{utilisateur.nom}', 'email': '{utilisateur.email}', 'role':'{utilisateur.role}'}}",
            level="info"
        )

    def delete_user(self, utilisateur):
        """
        Delete a user from the database.
        """
        self.repo.delete(utilisateur)
