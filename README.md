# Task Management System – JWT Authentication & Kafka Event-Driven Backend

A scalable backend Task Management System built using FastAPI, JWT Authentication, SQLite, and Apache Kafka.
The project demonstrates secure authentication workflows, REST API development, modular backend architecture, and asynchronous event-driven communication using Kafka producer-consumer pipelines.

The system allows users to register, securely log in, access protected APIs using JWT tokens, and perform CRUD operations on tasks while asynchronously publishing backend events through Kafka.

---

# Overview

Modern backend systems require secure authentication, scalable APIs, and asynchronous event handling for improved system reliability and modularity.

This project was built to simulate real-world backend engineering concepts commonly used in enterprise and fintech-grade applications.

The application combines:

* REST API development
* JWT-based authentication
* Event-driven architecture
* Kafka producer-consumer workflows
* Backend modularization
* Asynchronous processing

---

# Features

## Authentication & Security

* User registration and login
* JWT token generation and validation
* Protected API routes
* Password hashing using bcrypt/passlib
* Bearer token authentication

## Task Management

* Create tasks
* Fetch user tasks
* Update tasks
* Delete tasks
* User-specific task access

## Kafka Event Processing

* Kafka producer publishes task events
* Kafka consumer processes backend events asynchronously
* Event logging and background processing simulation

## Backend Architecture

* Modular FastAPI project structure
* Service-based architecture
* Schema validation using Pydantic
* Centralized configuration management

---

# Tech Stack

## Backend

* Python
* FastAPI
* REST APIs

## Authentication & Security

* JWT (JSON Web Tokens)
* bcrypt / passlib

## Database

* SQLite

## Event Streaming

* Apache Kafka
* aiokafka

## Validation & Utilities

* Pydantic
* Python Dotenv
* Uvicorn

## Tools & Platforms

* Git
* GitHub
* Visual Studio Code

---

# System Architecture

1. User registers and logs into the system
2. Backend validates credentials and generates JWT token
3. User accesses protected APIs using Bearer token authentication
4. Task CRUD operations performed through FastAPI endpoints
5. Kafka producer publishes task-related events
6. Kafka consumer asynchronously processes backend events
7. Responses returned through REST APIs

---

# Authentication Workflow

## User Registration

User registers using:

* Username
* Email
* Password

Passwords are securely hashed before database storage.

---

## User Login

Backend:

* Verifies password hash
* Generates JWT access token
* Returns Bearer authentication token

---

## Protected Routes

Authenticated requests require:

```http id="s9m2v1"
Authorization: Bearer <token>
```

JWT token is:

* decoded
* verified
* authenticated

before granting API access.

---

# Kafka Workflow

## Producer

After task operations:

* TASK_CREATED
* TASK_UPDATED
* TASK_DELETED

events are published to Kafka topics.

---

## Kafka

Kafka acts as a message broker between backend services by:

* receiving events
* storing messages
* managing asynchronous communication

---

## Consumer

Kafka consumer listens for task events and processes:

* logging
* event tracking
* notification simulation
* asynchronous workflows

---

# API Endpoints

## Authentication APIs

| Method | Endpoint         | Description   |
| ------ | ---------------- | ------------- |
| POST   | `/auth/register` | Register user |
| POST   | `/auth/login`    | Login user    |

---

## Task APIs

| Method | Endpoint      | Description      |
| ------ | ------------- | ---------------- |
| POST   | `/tasks`      | Create task      |
| GET    | `/tasks`      | Fetch tasks      |
| GET    | `/tasks/{id}` | Fetch task by ID |
| PUT    | `/tasks/{id}` | Update task      |
| DELETE | `/tasks/{id}` | Delete task      |

---

# Project Structure

```bash id="8u2kq4"
task-management-system/
│
├── app/
│   ├── auth/
│   ├── database/
│   ├── kafka/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# Core Functionalities

## JWT Authentication

* Secure stateless authentication
* Token generation and verification
* Protected route authorization

---

## REST API Development

* CRUD API implementation
* Request-response handling
* API validation and serialization

---

## Event-Driven Backend Processing

* Producer-consumer communication
* Kafka-based event streaming
* Asynchronous backend workflows

---

## Database Integration

* SQLite database operations
* User-task relationship management
* Persistent task storage

---

# Challenges Solved

* Secure authentication implementation
* Stateless JWT authorization flow
* Kafka integration with FastAPI
* Producer-consumer event handling
* Modular backend structuring
* API protection and validation

---

# Project Contribution

* Built modular FastAPI backend architecture
* Implemented JWT authentication workflows
* Developed protected REST APIs
* Integrated Kafka producer-consumer pipeline
* Designed SQLite database structure
* Implemented asynchronous event processing
* Structured scalable backend service layers

---

# Future Enhancements

* PostgreSQL integration
* Docker containerization
* Redis caching
* Role-based access control (RBAC)
* Email notification services
* Kubernetes deployment
* CI/CD pipeline integration

---

# Installation

## Clone Repository

```bash id="3pz8mf"
git clone <repository-url>
cd task-management-system
```

---

## Install Dependencies

```bash id="2jv1mc"
pip install -r requirements.txt
```

---

## Run Application

```bash id="0tk6wx"
uvicorn app.main:app --reload
```

---

## Swagger API Documentation

```bash id="e4s7py"
http://127.0.0.1:8000/docs
```

---

# Learning Outcomes

This project helped in understanding:

* REST API architecture
* JWT authentication workflows
* FastAPI backend development
* Kafka producer-consumer architecture
* Event-driven systems
* Stateless authentication
* CRUD API development
* Modular backend engineering
* Database integration and validation

---

# Author

### Aman Yahya Khan

AI/ML & Backend Systems Engineer
Pune, Maharashtra, India

GitHub: github.com/amankhan1310
