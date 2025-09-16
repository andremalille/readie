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
docker-compose up --build

3. Once the build is complete, open the application in your browser:
http://localhost:8000/

4. To stop the containers, press Ctrl + C in the terminal or run:
docker-compose down
