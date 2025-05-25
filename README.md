# School ERP System API

A FastAPI-based REST API for School ERP System management.

## Description

This project implements a RESTful API service for a School ERP System using FastAPI framework. It provides various endpoints for managing school-related operations with proper error handling and database integration.

## Features

- FastAPI framework with automatic API documentation
- SQL Database integration using SQLAlchemy
- CORS middleware enabled
- Comprehensive error logging
- Health check endpoints
- Database connection monitoring

## Technical Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL/MySQL (Database)
- Logging

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
+-- main.py                 # Main application entry point
+-- requirements.txt        # Project dependencies
+-- app/
    +-- db/                # Database related code
    ¦   +-- database.py    # Database connection and session management
    +-- log/               # Logging functionality
    ¦   +-- logException.py
    +-- model/             # Data models
        +-- errorLog.py
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health/database` - Database health check endpoint
- `GET /items/{item_id}` - Retrieve item by ID
- `GET /about` - About information
- `GET /callMenu/{menu_id}` - Retrieve menu by ID

## API Documentation

The API documentation is automatically generated and can be accessed at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/api/v1/openapi.json`

## Error Handling

The application includes comprehensive error handling:
- Database connection errors
- Resource not found errors
- Unexpected runtime errors
- All errors are properly logged

## Development

To run the development server:

```bash
uvicorn main:app --reload
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Add your license here]
