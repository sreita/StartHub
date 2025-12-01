# 🐳 Docker Deployment Guide - StartHub

This guide details the steps to install, configure, and run the **StartHub** platform using Docker containers. This architecture ensures the project runs identically on any machine, eliminating local version or dependency issues.

---

## 📋 1. Docker Installation

Before starting, you need the Docker engine installed on your machine.

### 🪟 For Windows

1. Download **Docker Desktop for Windows** from docker.com.
2. Run the installer. Ensure you check **"Use WSL 2 instead of Hyper-V"** (recommended for performance).
3. Once installed, restart your computer.
4. Open "Docker Desktop" and wait for the engine status to turn green/running.

### 🍎 For Mac (macOS)

1. Download **Docker Desktop for Mac** (Choose correct version: Intel chip or Apple Silicon M1/M2/M3).
2. Drag the icon to your Applications folder.
3. Open the app and grant necessary permissions.

### 🐧 For Linux (Ubuntu/Debian)

Run the following in your terminal:

```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# (Log out and log back in to apply user permissions)
```

---

## ⚙️ 2. Project Configuration

Before starting the containers, we need to configure secure credentials.

1. Navigate to the project root directory `StartHub/`.
2. Create a file named `.env` (no name, just the extension).
3. Paste the following content inside:

```ini
# Docker Database Configuration
DB_NAME=starthub_db
DB_PASSWORD=root #insecure configuration for now

# (Optional) Debug Configuration
APP_DEBUG=true
```

---

## 🚀 3. Running the Project

Follow these steps to spin up the entire infrastructure (Frontend, Backend, DB, and MailHog).

### Start Services

Open your terminal in the project root and run:

```bash
docker compose up --build
```

* **up**: Starts the containers.
* **--build**: Forces a rebuild of the code (Java/Python) to ensure latest changes are applied.

**Note:** The first run may take a few minutes as it downloads base images and compiles dependencies.

### Stop Services

To stop everything gracefully, press **Ctrl + C** in the terminal, or run in a new window:

```bash
docker compose down
```

### Full Reset (Delete Data)

If you want to wipe the database and start fresh (useful if data gets corrupted):

```bash
docker compose down -v
```

(The `-v` flag removes persistent data volumes).

---

## 🌐 4. Accessing Services

Once the terminal shows the logs and the system is stable, you can access:

| Service      | URL                                                      | Description                            |
| ------------ | -------------------------------------------------------- | -------------------------------------- |
| Frontend     | [http://localhost:3000](http://localhost:3000)           | Main Web Application                   |
| MailHog      | [http://localhost:8025](http://localhost:8025)           | Fake Email Inbox (Testing)             |
| FastAPI Docs | [http://localhost:8000/docs](http://localhost:8000/docs) | Data Backend Swagger UI                |
| Spring API   | [http://localhost:8081](http://localhost:8081)           | Authentication API                     |
| Database     | localhost:3306                                           | External Host (User: root, Pass: root) |

---

## 🏗️ 5. Technical Architecture

The project uses a microservices architecture orchestrated via Docker Compose.

### Components & Technologies

#### **Frontend (Nginx Alpine)**

* Ultra-lightweight web server serving static files (HTML/JS/CSS).
* Exposed Port: **3000** (mapped internally to 80).

#### **Spring Boot Auth (Java 21)**

* Multi-stage build:

  * Stage 1: Uses Maven to compile source code.
  * Stage 2: Uses a clean JRE image to run only the `.jar`, reducing size.
* Includes restart policy: `restart: on-failure`.

#### **FastAPI Data (Python 3.12)**

* Based on `python:3.12-slim`.
* Installs system libraries (`libmysqlclient-dev`) for MySQL.
* Runs inside a virtual environment (venv).

#### **Database (MySQL 8.0)**

* Persistent storage through **Docker Volumes**.
* Auto-initialization on first boot:

  * Schema (Tables)
  * Seeds (Users, Categories, Startups, Votes, etc.)

#### **MailHog**

* Fake SMTP server to capture registration/recovery emails.

