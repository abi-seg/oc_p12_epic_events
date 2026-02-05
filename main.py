from models.base import Base, engine
from sqlalchemy import text

# Placeholder - no models yet, we just test the connection
Base.metadata.create_all(engine)

print("Connexion réussie à la base de données MySQL.")

# To get the name of the DB
with engine.connect() as connection:
    result = connection.execute(text("SELECT DATABASE();"))
    db_name = result.scalar()
    print(f"Nom de la base de données : {db_name}")
    