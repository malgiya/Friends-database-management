# FastAPI Friends Management

A FastAPI application for managing friend records, including creating, updating, deleting, and viewing friends.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

## Features

- Create, update, delete, and view friend records.
- Organized route handling using FastAPI routers.
- User authentication and authorization (if implemented).
- SQLAlchemy for database interactions.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` file in the root directory and add your environment variables:**

    ```env
    DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
    SECRET_KEY=your-secret-key
    ```

2. **Update the `DATABASE_URL` with your actual database connection string.**

## Usage

1. **Run the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    - `app.main:app` specifies the FastAPI application instance.
    - The `--reload` flag enables auto-reloading of code changes.

2. **Access the API documentation at:**

    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

- **Create a Friend**: `POST /friends/`
- **Get a Friend**: `GET /friends/{friend_id}`
- **Update a Friend**: `PUT /friends/{friend_id}`
- **Delete a Friend**: `DELETE /friends/{friend_id}`
- **View All Friends**: `GET /friends/`

Refer to the API documentation for detailed information about request parameters and responses.

## Testing

1. **Run tests:**

    ```bash
    pytest
    ```

    Ensure that you have `pytest` installed and properly configured.

## Deployment

To deploy the application:

1. **Prepare your environment for deployment (e.g., configure your cloud provider).**
2. **Push your code to the cloud service (e.g., AWS, Vercel, Heroku).**
3. **Follow the specific deployment instructions for your chosen platform.**

Refer to your cloud provider’s documentation for detailed deployment instructions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
