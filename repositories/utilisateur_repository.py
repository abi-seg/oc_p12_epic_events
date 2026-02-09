from models.utilisateur import Utilisateur
from models.base import Session


class UtilisateurRepository:
    """
    Repository class responsible for managing Utlisateur entities.
    This class provides methods to interact with the database session
    for creating and retrieving Utilisateur entities.

    """

    def __init__(self, session):
        """
        Initializes the repository with a SQLALchemy session.
        :param session: SQLALchemy session used for database operations.
        """
        self.session = session

    def find_by_email(self, email):
        """
        Retrieves a Utilisateur by their email address.

        :param email: Email address to search for.
        :type email: str
        :return: The matching utilisateur instance if found, otherwise none.

        """
        return self.session.query(Utilisateur).filter_by(email=email).first()

    def save(self, utilisateur):
        """
        Saves a utilisateur entity to the database.
        The entity is added to the current session and committed immediately.

        :param utilisateur: Utilisateur instance to save.

        """
        self.session.add(utilisateur)
        self.session.commit()

    def get_all(self):
        """
        Fetch all users from the database.
        :return: List of Utilisateur objects

        """
        return self.session.query(Utilisateur).all()
