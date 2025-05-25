from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pyodbc

# Using Windows Authentication with pyodbc
# This connection string uses trusted connection which is ideal for Windows Authentication
DATABASE_URL = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};Server=(localdb)\\MSSQLLocalDB;Database=schoolErp;Trusted_Connection=yes;MultipleActiveResultSets=True"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    # Test the connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {str(e)}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()