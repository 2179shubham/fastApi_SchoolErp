
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.db.database import get_db
from app.log.logException import log_error_to_db


router = APIRouter()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/checkdatabaseconnection")
async def check_db_connection(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Database connection is working properly"
        }
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {str(e)}")
        log_error_to_db(e)
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection failed",
                "error": str(e)
            }
        )