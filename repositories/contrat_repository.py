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
