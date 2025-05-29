from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging
from fastapi.openapi.utils import get_openapi

from app.log.logException import log_error_to_db
from app.db.database import get_db
from app.middleware.JWTBearer import JWTBearer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_handler = JWTBearer()

app = FastAPI(
    title="School ERP API",
    description="School ERP System API documentation",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Swagger UI authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API Description",
        routes=app.routes,
    )

    # Add security scheme to OpenAPI schema
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Add global security requirement
    openapi_schema["security"] = [
        {
            "Bearer": []
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/protected")
async def protected_route(payload: dict = Depends(auth_handler)):
    return {"message": "You have access!", "user_data": payload}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health/database", tags=["Health Check"])
async def check_db_connection(db: Session = Depends(get_db)):
    """
    Check if the database connection is working.
    Returns:
        dict: A dictionary containing the status of the database connection
    """
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
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection failed",
                "error": str(e)
            }
        )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/about")
def health_check():
    return {"about_check": "returned successfully"}

@app.get("/callMenu/{menu_id}")
def call_menu(menu_id: int, db: Session = Depends(get_db)):

    try:
        stmt = text("SELECT * FROM Menu WHERE MenuID = :menu_id")
        result = db.execute(stmt, {"menu_id": menu_id})
        row = result.fetchone()
        print("result of data", row)
        
        if row is None:
            raise HTTPException(status_code=404, detail="Menu not found.")
            
        # Convert SQLAlchemy Row to dictionary using _mapping attribute
        return dict(row._mapping)

    except SQLAlchemyError as e:
        error_detail = f"Database error while fetching menu with MenuId {menu_id}: {e}"
        logger.error(error_detail)
        raise HTTPException(
            status_code=500,
            detail="A database error occurred while fetching the menu. Please try again later."
        )
    except Exception as e:
        error_detail = f"Unexpected error while fetching menu with MenuId {menu_id}: {e}"
        logger.error(error_detail)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please contact support."
        )

