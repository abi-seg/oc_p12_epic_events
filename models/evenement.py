from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True)

    contrat_id = Column(Integer, ForeignKey("contrats.id"))
    support_id = Column(Integer, ForeignKey("utilisateurs.id"))

    nom_client = Column(String(100))
    contact_client = Column(String(100))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    lieu = Column(String(255))
    participants = Column(Integer)
    notes = Column(Text)

    contrat = relationship("Contrat", back_populates="evenements")
    support = relationship("Utilisateur", back_populates="evenements")
