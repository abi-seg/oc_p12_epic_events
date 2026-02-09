from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from models.client import Client
from models.contrat import Contrat
from models.evenement import Evenement


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)

    # Un commercial peut avoir plusieurs clients
    clients = relationship("Client", back_populates="commercial")
    contrats = relationship("Contrat", back_populates="commercial")

    # Un utilisateur support peut avoir plusieurs evenements
    evenements = relationship("Evenement", back_populates="support")

    def __repr__(self):
        return f"<Utilisateur(nom={
            self.nom}, email={
            self.email}, role={
            self.role})>"
