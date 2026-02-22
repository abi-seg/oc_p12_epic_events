from models.evenement import Evenement
from repositories.evenement_repository import EvenementRepository


class EvenementService:
    """
    Service layer responsible for business logic related to events (Evenements).
    """

    def __init__(self, session):
        """
        Initialize the event service with a database session.
        """
        self.repo = EvenementRepository(session)

    def create_evenement(
            self,
            contrat_id: int,
            nom_client: str,
            contact_client: str,
            date_debut,
            date_fin,
            lieu: str,
            participants: int,
            notes: str = None,
            support_id: int = None,
    ):
        """
        Create a new event and persist it to the database.
        """
        evenement = Evenement(
            contrat_id=contrat_id,
            support_id=support_id,
            nom_client=nom_client,
            contact_client=contact_client,
            date_debut=date_debut,
            date_fin=date_fin,
            lieu=lieu,
            participants=participants,
            notes=notes,

        )
        self.repo.save(evenement)
        return evenement

    def get_all_evenements(self):
        """
        Retrieve all events from the database.
        """
        return self.repo.get_all()

    def get_evenements_by_support_id(self, support_id: int):
        """
        Retrieve all events assigned to a specific support user.
        """
        return self.repo.get_by_support_id(support_id)

    def get_evenement_by_id(self, evenement_id: int):
        """
        Retrieve an event by its identifier.
        """
        return self.repo.get_by_id(evenement_id)

    def update_evenement(self, evenement, **fields):
        """
        update an existing event with the given field values and persist changes.

        Parameters
            evenement: Evenement
                The event instance to update.
            **fields:
                Arbitary keyword arguments mapping attribute names to new values.
        """
        for attr, value in fields.items():
            if value is not None:
                setattr(evenement, attr, value)
        self.repo.update(evenement)
