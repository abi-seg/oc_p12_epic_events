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
