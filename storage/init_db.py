from storage.db import Base, engine
from storage.models import PricingRecord

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Database initialized.")
