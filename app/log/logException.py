# main.py

from datetime import datetime
import logging

from app.db.database import SessionLocal
from app.model.errorLog import ErrorLog
# Use the Uvicorn logger (or configure your own)
logger = logging.getLogger("uvicorn.error")

def log_error_to_db(error_details: str):
    """
    Log error details into the `errorlog` table.
    """
    session = SessionLocal()  # Create a new session for logging errors
    try:
        # Create an instance of the ErrorLog model
        error_log = ErrorLog(details=error_details, createddate=datetime.utcnow())
        session.add(error_log)
        session.commit()
    except Exception as log_exc:
        # If logging to the database fails, log it to the standard logger.
        session.rollback()
        logger.error("Failed to log error to the errorlog table: %s", log_exc)
    finally:
        session.close()
