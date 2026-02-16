from models.client import Client
from repositories.client_repository import ClientRepository
from datetime import date


class ClientService:

    """
    Service layer responsible for user-related business logic.

    This class handles client creation and delegates
    presistance operations to the ClientRepository.

    """

    def __init__(self, session):
        """
        Initialize the client service with a database session.
              :param session: SQLALchemy session used to access the repository.

        """
        self.repo = ClientRepository(session)

    def create_client(self, nom_complet, email, phone, entreprise, commercial_id):
        """
        Create a new client and persist it to the database.

        Parameters
        ----------
        nom_complet : str
            The full name of the client contact.
        email : str
            The email address of the client.
        phone : str
            The phone number of the client.
        entreprise : str
            The company name associated with the client.
        commercial_id : int
            The identifier of the commercial (Utilisateur) responsible
            for this client.

        Returns
        -------
        Client
            The newly created and saved Client instance.
        """
        client = Client(
            nom_complet=nom_complet,
            email=email,
            telephone=phone,
            entreprise=entreprise,
            date_creation=date.today(),
            commercial_id=commercial_id
        )
        self.repo.save(client)
        return client

    def get_all_clients(self):
        """
        Retrieve all clients from the database.

        Returns: A list containing all the saved Client entities.

        """
        return self.repo.get_all()

    def get_clients_by_commercial_id(self, commercial_id):
        """
        Retrieve all clients assigned to a specific commercial user.

        Returns:
            A list of Client entities linked to the given commercial_id.

        """
        return self.repo.get_by_commercial_id(commercial_id)

    def get_client_by_id(self, client_id):
        """
        Retrieve a client by its identifier.

        Parameters
        ----------
        client_id : int
        The primary key of the client to retrieve.

        Returns : The Client instance if found, otherwise None.
    """
        return self.repo.get_by_id(client_id)

    def update_client(self, client, **fields):
        """
        Update an existing client with the given field values and persist changes.

        Parameters
        ----------
        client : Client
        The Client instance to update.
     **fields :
        Arbitrary keyword arguments mapping attribute names to new values
        (for example: email="new@mail.com", telephone="06 12 34 56 78").

        Notes
        -----
        This method applies the provided field updates to the client object
        and delegates persistence to the repository's update method.
        """
        for attr, value in fields.items():
            if value is not None:
                setattr(client, attr, value)
        self.repo.update(client)

    def delete_client(self, client):
        self.repo.delete(client)
