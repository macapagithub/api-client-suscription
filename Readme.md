# API Client Subscription Management

This project is a FastAPI application designed to manage clients and their subscriptions to various services or plans. It provides a RESTful API for creating, reading, updating, and deleting clients and subscriptions, as well as associating clients with specific subscriptions.

## Project Structure

```
api-client-suscription/
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── conftest.py         # Pytest configuration file, for fixtures and plugins
├── db.sqlite3          # SQLite database file
├── main.py             # Main application file, FastAPI app initialization and router inclusion
├── requirements.txt    # Python package dependencies
├── app/                # Core application logic
│   ├── __init__.py
│   ├── db.py           # Database setup (SQLModel) and session management
│   ├── dependencies.py # FastAPI dependency functions (e.g., for fetching objects or 404)
│   ├── models.py       # SQLModel data models (Client, Suscription, ClientSuscription)
│   └── routers/        # API endpoint definitions
│       ├── __init__.py
│       ├── clients.py      # Routers for client and client-subscription operations
│       └── suscriptions.py # Routers for subscription plan operations
├── env-fast/           # Python virtual environment (example name)
└── tests/              # Automated tests for the application
    ├── __init__.py
    └── test_client.py  # Example test file for client endpoints
```

## Key Technologies

*   **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python.
*   **SQLModel**: Library for interacting with SQL databases from Python code, with Python objects. It is designed to be compatible with Pydantic and SQLAlchemy.
*   **Uvicorn**: ASGI server for running FastAPI applications.
*   **Pytest**: Framework for writing and running tests.
*   **SQLite**: Self-contained, serverless, zero-configuration, transactional SQL database engine.

## Setup and Running the Application

### Prerequisites

*   Python 3.11 or higher
*   `pip` (Python package installer)
*   Git (for cloning the repository)

### Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd api-client-suscription
    ```

2.  **Create and activate a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv env
    ```
    Activate the environment:
    *   On macOS and Linux:
        ```bash
        source env/bin/activate
        ```
    *   On Windows:
        ```bash
        env\Scripts\activate
        ```

3.  **Install dependencies:**
    Install the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the FastAPI application locally for development, use the `fastapi dev` command (provided by `fastapi-cli`, which should be in `requirements.txt`):

```bash
fastapi dev main.py
```

Alternatively, you can use `uvicorn` directly:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reloading when code changes are detected, which is useful for development.

### Accessing the API

*   **API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **Alternative API Docs (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

The application exposes the following main groups of endpoints:

### Clients

Managed in [`app/routers/clients.py`](app/routers/clients.py).

*   `POST /clients/`: Create a new client.
*   `GET /clients/`: Retrieve a list of all clients.
*   `GET /clients/{client_id}`: Retrieve a specific client by ID.
*   `PATCH /clients/{client_id}`: Update an existing client.
*   `DELETE /clients/{client_id}`: Delete a client.

### Subscriptions (Plans)

Managed in [`app/routers/suscriptions.py`](app/routers/suscriptions.py).

*   `POST /suscriptions/`: Create a new subscription plan.
*   `GET /suscriptions/`: Retrieve a list of all subscription plans.

### Client Subscriptions

Managed in [`app/routers/clients.py`](app/routers/clients.py).

*   `POST /clients/{client_id}/suscribe/{suscription_id}`: Subscribe a client to a specific subscription plan. Requires a `suscription_status` query parameter (e.g., `active`, `inactive`, `cancelled`).
*   `GET /clients/{client_id}/suscriptions`: Retrieve all subscriptions for a specific client. Can be filtered by `suscription_status` query parameter.

## Running Tests

The project uses Pytest for testing. To run the tests:

```bash
pytest
```

Ensure your virtual environment is activated and all development dependencies are installed. Test files are located in the `tests/` directory, such as [`tests/test_client.py`](tests/test_client.py).

## Database

The application uses SQLite as its database, with the database file being `db.sqlite3`. SQLModel is used as the ORM to interact with the database and define models in [`app/models.py`](app/models.py).
The database connection and session management are handled in [`app/db.py`](app/db.py).

