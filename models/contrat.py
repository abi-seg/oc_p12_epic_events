from sqlalchemy import Column, Integer, DECIMAL, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Contrat(Base):
    __tablename__ = "contrats"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id"))
    commercial_id = Column(Integer, ForeignKey("utilisateurs.id"))

    montant_total = Column(DECIMAL(10, 2))
    montant_restant = Column(DECIMAL(10, 2))
    date_creation = Column(Date)
    statut = Column(Boolean)  # True = signé, False = non signé

    client = relationship("Client", back_populates="contrats")
    commercial = relationship("Utilisateur", back_populates="contrats")
