from models.evenement import Evenement


class EvenementRepository:
    """
    Data access layer for Evenement entities using SQLALchemy ORM.
    """

    def __init__(self, session):
        """
        Initialize the repository with a SQLALchemy session.
        """
        self.session = session

    def save(self, evenement: Evenement):
        """
        Persist a new Evenement to the database and refresh it.
        """
        self.session.add(evenement)
        self.session.commit()
        self.session.refresh(evenement)
        return evenement

    def get_all(self):
        """
        Retrieve all evenements from the database.
        """
        return self.session.query(Evenement).all()
