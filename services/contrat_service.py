# services/contrat_service.py

from models.contrat import Contrat
from repositories.contrat_repository import ContratRepository
from datetime import date


class ContratService:
    """
    Service layer responsible for business logic related to contracts (Contrats).
    This class handles operations such as contract creation, filtering, and updates.
    """

    def __init__(self, session):
        """
        Initialize the contract service with a database session.

        :param session: SQLAlchemy session used to initialize the repository.
        """
        self.repo = ContratRepository(session)

    def create_contrat(self, client_id, commercial_id, montant_total, montant_restant=None, statut=False):
        """
        Create and save a new contract.

        Parameters
        ----------
        client_id : int
            The ID of the client this contract belongs to.
        commercial_id : int
            The ID of the commercial associated with this contract.
        montant_total : float
            The total amount of the contract.
        montant_restant : float or None
            The remaining amount to be paid. Defaults to montant_total if not provided.
        statut : bool
            Indicates whether the contract has been signed. Default is False.

        Returns
        -------
        Contrat
            The newly created and persisted contract instance.
        """
        if montant_restant is None:
            montant_restant = montant_total

        contrat = Contrat(
            client_id=client_id,
            commercial_id=commercial_id,
            montant_total=montant_total,
            montant_restant=montant_restant,
            date_creation=date.today(),
            statut=statut
        )
        self.repo.save(contrat)
        return contrat

    def get_all_contrats(self):
        """
        Retrieve all contrats from the database.
        """
        return self.repo.get_all()

    def get_contrats_by_commercial_id(self, commercial_id: int):
        """
        Retrieve all contrats associated with a given commercial user.
        """
        return self.repo.get_by_commercial_id(commercial_id)

    def get_contrat_by_id(self, contrat_id: int):
        """
        Retrieve a contract by its identifier.
        """
        return self.repo.get_by_id(contrat_id)

    def update_contrat(self, contrat: Contrat, **fields):
        """
        Update an existing contract with the given field values and presist changes.
        Parameters:
            contrat : Contrat
                The Contrat instance to update.
            **fields: 
                Arbitrary key arguments mapping attribute names to new values.
        """
        for attr, value in fields.items():
            if value is not None:
                setattr(contrat, attr, value)
        self.repo.update(contrat)

    def delete_contrat(self, contrat: Contrat):
        """
        Delete a contract from the database.
        """
        self.repo.delete(contrat)

    def get_unsigned_contrats(self):
        """
        Get all contrats that are not signed.
        """
        return self.repo.get_by_staut(False)

    def get_unpaid_contrats(self):
        """
        Get all contrats where montant_restant > 0.
        """
        return self.repo.get_unpaid()
