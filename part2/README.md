# HBnB

HBnB is a web application that provides a platform for users to list, discover, and review places to stay. It offers features like user management, place listings, reviews, and amenities.

## Project Structure

```plaintext
hbnb/
└── app/                           ➔ Main application package
    ├── __init__.py                  - Initializes the Flask app and API
    ├── api/                         - API routes and endpoints
    │   ├── __init__.py              - Initializes the API package
    │   └── v1/                    ➔ Version 1 of the API
    │       ├── __init__.py          - Initializes version 1 of the API
    │       ├── users.py             - Endpoints for user management
    │       ├── places.py            - Endpoints for managing places (listings)
    │       ├── reviews.py           - Endpoints for handling reviews and ratings
    │       └── amenities.py         - Endpoints for managing amenities
    ├── models/                    ➔ Data models for the application
    │   ├── __init__.py              - Initializes the models package
    │   ├── user.py                  - User model definition
    │   ├── place.py                 - Place model definition
    │   ├── review.py                - Review model definition
    │   └── amenity.py               - Amenity model definition
    ├── services/                  ➔ Business logic and application services
    │   ├── __init__.py              - Initializes the services package
    │   └── facade.py                - Facade pattern for orchestrating complex operations
    └── persistence/               ➔ Data persistence layer
        ├── __init__.py              - Initializes the persistence package
        └── repository.py            - Database interaction and repository pattern
├── run.py                         ➔ Entry point to start the Flask application
├── config.py                      ➔ Configuration settings (e.g., environment variables)
├── requirements.txt               ➔ List of Python dependencies to install
└── README.md                      ➔ Project documentation and usage instructions
```
## Install Required Packages

Make sure you have Python installed on your system. 
Install the required packages using:

```bash
pip install -r requirements.txt
```

## Run the Application

To start the application, use one of the following commands:

```bash
python run.py
```

or:

```bash
python3 run.py
```
