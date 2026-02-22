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

    def get_by_support_id(self, support_id: int):
        """
        Retrieve all events assigned to a specific support user.
        """
        return (
            self.session
            .query(Evenement)
            .filter(Evenement.support_id == support_id)
            .all()
        )

    def get_by_id(self, evenement_id: int):
        """
        Retrieve an event by its identifier.
        """
        return self.session.query(Evenement).get(evenement_id)

    def update(self, evenement: Evenement):
        """
        Persist changes made to an existing event.
        """
        self.session.commit()
        self.session.refresh(evenement)
        return evenement
