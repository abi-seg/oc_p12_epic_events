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
