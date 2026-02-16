from models.client import Client
from models.base import Session


class ClientRepository:
    """
    Repository class responsible for managing Client entities.
    Tis class provides methods to interact with the database sesssion
    for creating and retrieving client entities.

    """

    def __init__(self, session):
        """
        Initialize the repository with a database session.

        Parameters
        session: Session
            An SQLALchemy session used to interact with the database.

        """

        self.session = session

    def save(self, client):
        """
        Save a client entity and commit the transaction.

        Parameters
        client: Client
            The client instance to be added or updated in the database.

        """
        self.session.add(client)
        self.session.commit()

    def get_all(self):
        """
        Retrieve all clients from the database.

        Returns: A list containing all client records.

        """
        return self.session.query(Client).all()

    def get_by_commercial_id(self, commercial_id):
        """
        Retrieve all clients assigned to a specific commercial user.

        Parameters
        commercial_id : The identifier of the commercial (Utilisateur) responsible
        for the clients.

        Returns:
            A list of Client records linked to the given commercial_id.

        """
        return self.session.query(Client).filter_by(commercial_id=commercial_id).all()

    def get_by_id(self, client_id):
        """
        Retrieve a single client by its identifier.
        Parameters:
            client_id : int
            Primary key of the client to load.
        Returns
            The matching client instance if found,otherwise none.
        """
        return self.session.query(Client).filter_by(id=client_id).first()

    def update(self, client):
        """
        Saves the pending changes for the given client to the database.

        Parameters
           client : Client
           The client instance whose modifications have already been applied to the 
           SQLALchemy session.
       """
        self.session.commit()

    def delete(self, client):
        self.session.delete(client)
        self.session.commit()
