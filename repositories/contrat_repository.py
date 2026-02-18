from models.contrat import Contrat


class ContratRepository:
    """
    Data access layer for Contrat entities using SQLALchemy ORM.

    """

    def __init__(self, session):
        """
        Initialize with SQLALchemy session.
        Parameters:
            session : sqlalchemy.orm.session
                A session object for DB communication.
        """
        self.session = session

    def save(self, contrat):
        """
        Persist a new contrat to the database and refresh it.

        """
        self.session.add(contrat)
        self.session.commit()
        self.session.refresh(contrat)
        return contrat

    def get_all(self):
        """
        Retrieve all contracts from the database.
        """
        return self.session.query(Contrat).all()

    def get_by_commercial_id(self, commercial_id: int):
        """
        Retrieve all contracts associated with a given commercial.
        Parameters:
            commercial_id : int
            The ID of the commercial user.
        Returns: list of contrats
        """
        return (
            self.session
            .query(Contrat)
            .filter(Contrat.commercial_id == commercial_id)
        )

    def get_by_id(self, contrat_id: int):
        """
        Retrieve a contract by its identifier.
        """
        return self.session.query(Contrat).get(contrat_id)

    def update(self, contrat: Contrat):
        """
        Persist changes made to an existing contract.
        """
        self.session.commit()
        self.session.refresh(contrat)
        return contrat

    def delete(self, contrat: Contrat):
        """
        Delete a contrat from the database.
        """
        self.session.delete(contrat)
        self.session.commit()
