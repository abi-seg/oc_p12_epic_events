from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import logging
# charger .env
load_dotenv()

# Charger l'URL de la base
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(" DATABASE_URL est manquant dans .env")

# Moteur SQLALchemy
engine = create_engine(DATABASE_URL, echo=False)

# session locale
Session = sessionmaker(bind=engine)
# removes the sql log in console.
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

# Base commune pour les modèles
Base = declarative_base()
