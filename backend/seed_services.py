from backend.database.connection import SessionLocal
from backend.database.models import Service

def seed_master_services():
    # 🗄️ 1. Start a conversation with the database
    db = SessionLocal()
    
    try:
        # 🕵️‍♂️ 2. Prevent duplicates by checking if data exists
        if db.query(Service).first() is not None:
            print("Services table already has data. Skipping seed script!")
            return

        print("Seeding car detailing master packages...")

        executive = Service(
            name="Executive Exterior Wash",
            price=75,
            description=""
        )

        # 🧼 3. Instantiate your definition objects
        bronze = Service(
            name="Bronze Express Wash",
            price=50,
            description="A quick exterior refresh to keep your car shining."
        )
        
        silver = Service(
            name="Silver Tier Interior",
            price=75,
            description="A detailed interior cleaning to keep your car smelling fresh."
        )
        
        gold = Service(
            name="Gold Tier",
            price=150,
            description="Premium package offering full exterior preservation alongside deep interior conditioning."
        )

        # 📥 4. Stage and permanently save the records
        db.add_all([executive, bronze, silver, gold])
        db.commit()
        print("Success! Executive, Bronze, Silver, and Gold services have been inserted.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred during seeding: {e}")
    finally:
        # 🧼 5. Free up database connection resources
        db.close()

if __name__ == "__main__":
    seed_master_services()