from app.db.database import Base, engine
from app.models.user import UserDB
from app.models.expense import ExpenseDB


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
