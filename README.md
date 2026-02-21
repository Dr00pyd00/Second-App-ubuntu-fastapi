# Mini Blog API

A REST API for a blog application : wit FastAPI and PostgreSQL.  
**[Live_demo](https://fastapi-blog-hneb.onrender.com)**

## Tech Stack

- Python 3.12 / FastAPI
- PostgreSQL (database)
- SQLAlchemy (orm)
- Alembic (migrations/updates models)
- JWT (authentication)
- Docker (deploiement)
- Pytest 

## Features

### Models
- Soft delete system
- status (active, archiver, signaled)
- ROle-based control (ie: only owner can delete a post)

#### Users
- registration
- authentication with JWT token


#### Posts
- CRUD 
- separated services/routes 
- pagination for posts listing

**Automated tests with pytest**


## How to run

### Prerequisites
- Docker
- Docker compose

### Setup

1. Clone the repositry
```bash 
