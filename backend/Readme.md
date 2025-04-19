# Balance Scale Game Backend

Welcome to the backend API for the **Balance Scale Game**, a robust FastAPI-powered service designed to support an educational game where players balance scales using a limited set of weights. This backend handles game logic, user authentication, and data management, providing a scalable foundation for the game’s frontend.

![Balance Scale Game Backend Diagram](https://res.cloudinary.com/dz3aj0ti8/image/upload/v1745086380/Screenshot_2025-04-19_at_11.42.46_PM_yxlfcv.png)  
ERD for database 

## API Reference
https://mathtastic.onrender.com/docs

## Table of Contents
- [About](#about)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Development](#development)


## About
This FastAPI backend powers the Balance Scale Game, an interactive tool for teaching addition and problem-solving. It provides RESTful APIs to manage game states, authenticate users, and store progress, built with scalability and security in mind. The backend is designed to integrate with a frontend (e.g., Vue.js) and can be deployed on platforms like Render.com.

## Features
- **User Authentication**: JWT-based authentication for secure user sessions.
- **Game Logic API**: Endpoints to calculate balance solutions with up to two weights.
- **Database Integration**: Supports PostgreSQL for storing user data and game progress.
- **Environment Configuration**: Uses `.env` files for environment-specific settings (dev, prod, test).
- **API Documentation**: Automatic Swagger UI and ReDoc via FastAPI.
- **Testing**: Includes Pytest for unit and integration tests.
- **Deployment Ready**: Configured with Docker for production deployment.

## Prerequisites
- Python 3.8+
- Docker (for containerized deployment)
- Git

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PORT`

`FRONTEND_HOST`

`SECRET_KEY`

`DB_URI`

`DB_PASSWORD`

Firebase credentials

`TYPE`
`PROJECT_ID`
`PRIVATE_KEY_ID`
`PRIVATE_KEY`
`CLIENT_EMAIL`
`CLIENT_ID`
`CLIENT_X509_CERT_URL`

## Run Locally

Clone the project

```bash
  git clone https://github.com/Csb-218/MathTastic.git
```

Go to the backend

```bash
  cd backend
```

activate virtual environment
```bash
source .venv/bin/activate
````

start server

```bash
fastapi dev main.py
```



## Running Tests

To run tests, run the following command

```bash
  cd backend
```
```bash
  pytest tests
```
