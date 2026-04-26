
# TaskFlow – Python To-Do Web Application

TaskFlow is a lightweight, containerized To-Do web application built using **Python (Flask)** and **Docker Compose**.  
The project demonstrates how a simple web application can be packaged, deployed, and managed consistently using containerization and version control tools.

---

## 📌 Project Overview

This application allows users to manage daily tasks through a simple web interface.  
It is designed as a learning project to understand:

- Web application development using Flask
- Containerization using Docker
- Multi-container management using Docker Compose
- Version control and collaboration using Git & GitHub

The application stores tasks in a local JSON file (`todos.json`), ensuring persistence even after container restarts.

---

## ✨ Features

- ➕ Add new tasks through a web form
- 📋 View all tasks in a structured UI
- ✔ Mark tasks as completed or pending
- ❌ Delete tasks permanently
- 📊 Live task statistics (Total, Pending, Completed)
- 💾 Persistent storage using JSON file
- ⚡ Simple and responsive interface

---

## 🐳 Containerization using Docker

The project is fully containerized to ensure consistent execution across environments.

### 🔹 Dockerfile

- Built on `python:3.10-slim` base image
- Installs dependencies from `requirements.txt`
- Copies application source code into the container
- Exposes port `5000`
- Runs the application using `python app.py`

### 🔹 Docker Compose

Docker Compose is used to simplify deployment and manage the application as a service.

Key functionalities:
- Builds Docker image automatically
- Maps host port `5000` to container port `5000`
- Mounts project directory for live development updates
- Enables one-command startup:

```bash id="docker1"
docker compose up --build
````

---

## 🔧 Git & GitHub Workflow

The project uses Git for version control and GitHub for remote repository management.

### 🔹 Commands Used

Initialize repository:

```bash id="git1"
git init
```

Track files:

```bash id="git2"
git add .
```

Save changes:

```bash id="git3"
git commit -m "Initial commit - TaskFlow Flask Docker App"
```

Connect to GitHub:

```bash id="git4"
git remote add origin https://github.com/<username>/python-todo-docker.git
```

Push to GitHub:

```bash id="git5"
git branch -M main
git push -u origin main
```

---

## 🚀 Running the Application

### Using Docker (Recommended)

```bash id="run1"
docker compose up --build
```

### Access the Application

```
http://localhost:5000
```

---

## 👤 Author

**Avani Shaji**
GitHub: [https://github.com/avanishaji](https://github.com/avanishaji)

---

## 📌 Summary

TaskFlow demonstrates a complete development workflow combining:

* Flask web development
* Docker containerization
* Docker Compose orchestration
* Git & GitHub version control

```

---





