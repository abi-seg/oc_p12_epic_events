from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    nom_complet = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telephone = Column(String(20))
    entreprise = Column(String(100))
    date_creation = Column(Date)
    date_mise_a_jour = Column(Date)

    # Lien avec utilisateur (commercial)
    commercial_id = Column(Integer, ForeignKey("utilisateurs.id"))

    # Relation vers l'objet utilisateur
    commercial = relationship("Utilisateur", back_populates="clients")
    contrats = relationship("Contrat", back_populates="client")
