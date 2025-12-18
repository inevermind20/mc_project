from db.database import Base, engine
from models import user, client, equipment, proposal, assistance, calendar

print("A criar todas as tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")
