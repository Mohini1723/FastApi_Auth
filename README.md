# FastAPI Authentication System with MongoDB

This is a robust authentication system built with FastAPI and MongoDB (Motor). It features user registration, secure login with JWT tokens, and password hashing using Bcrypt.

## Features

- **User Registration**: Sign up with email and password (hashed securely).
- **Authentication**: Login to receive a JWT access token.
- **Protected Routes**: Example protected endpoint accessible only with a valid token.
- **Async Database**: Uses `motor` for asynchronous MongoDB interactions.
- **MVC/MVP Structure**: Organized code structure (Schemas, Routers, Core Logic).

## Tech Stack

- **FastAPI**: Modern, high-performance web framework for building APIs.
- **MongoDB & Motor**: NoSQL database with async driver.
- **Bcrypt**: For secure password hashing.
- **PyJWT**: For JSON Web Token (JWT) handling.
- **Pydantic**: For data validation and schemas.

## Project Structure

```
app/
├── routers/
│   └── auth.py       # API endpoints (Register, Login, Me)
├── __init__.py
├── auth.py           # Core auth logic (Hash, Verify, JWT)
├── database.py       # Database connection
├── main.py           # Application entry point
└── schemas.py        # Pydantic models (Request/Response schemas)
requirements.txt      # Project dependencies
test_auth.py          # Automated verification script
```

## Setup & Installation

1. **Clone the repository** (if applicable) or navigate to project directory.

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **MongoDB**: Ensure you have MongoDB running locally on port `27017` or set the `MONGO_URL` environment variable.

## Running the Application

Start the server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API docs are at `http://127.0.0.1:8000/docs`.

## Verification

Run the automated test script to verify the authentication flow:

```bash
python test_auth.py
```
