## **Readie** is a web application for managing your personal library and reading process.  
This README provides instructions on how to run the project locally.

---

## Run locally with Docker

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed  
- [Docker Compose](https://docs.docker.com/compose/install/) installed  

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/andremalille/readie.git
   cd readie
   
2. Build and start the containers:
   ```bash
   docker-compose up --build

4. Once the build is complete, open the application in your browser:
   ```bash
   https://localhost:8000/

5. To stop the containers, press Ctrl + C in the terminal or run:
   ```bash
   docker-compose down

---

## Features
- User authentication – registration, login, and profile management.
- Book search – find books by title, author, genre or isbn.
- Personal library – add, edit, or remove books, toggle them favourite.
- Reading progress tracking – update number of pages read.
- Book lists – organize books into categories: Read later, Currently reading, Finished, On hold, Re-reading, Dropped reading.
- Admin panel – superuser access to manage users and global content.

## Non-Functional Requirements
- Performance: The system provides fast responses under normal usage.
- Scalability: The system can grow to handle more users and books without major performance issues.
- Reliability: Data safety and quick recovery after failures.
- Security: Password hashing, HTTPS communication.
- Maintainability: Easy updates via Git and Docker.
- Usability: Adaptive, user-friendly UI.

## Tech Stack
- Backend: Django (Python)
- Database: PostgreSQL (via psycopg2)
- Frontend: Django Templates (HTML, CSS, JS)
- Image handling: Pillow
- Code style: flake8
- Containerization: Docker
