# Premium Based API

A FastAPI-based machine learning application for premium prediction. The project provides a REST API for making predictions and includes a Streamlit frontend for interacting with the model. The application is containerized using Docker for easy deployment and can be deployed on cloud platforms such as AWS EC2.

---

## 🚀 Features

- FastAPI backend for prediction APIs
- Streamlit frontend for interactive predictions
- Dockerized application
- Easy deployment on AWS EC2
- REST API support
- Machine Learning model integration

---

## 🛠 Tech Stack

- Python
- FastAPI
- Streamlit
- Docker
- Machine Learning
- AWS EC2

---

# Pull Docker Image
hub.docker.com/r/nipun1a/premium-based-api
```bash
docker pull nipun1a/premium-based-api:latest
```

---

# Run Docker Container

```bash
docker run -d \
-p 8000:8000 \
-p 8501:8501 \
--name premium-api \
nipun1a/premium-based-api:latest
```

If your Docker image exposes different ports, modify the command accordingly.

---

# Verify Running Container

```bash
docker ps
```

---

# Stop Container

```bash
docker stop premium-api
```

---

# Start Existing Container

```bash
docker start premium-api
```

---

# Remove Container

```bash
docker rm -f premium-api
```

---

# Run Locally

## Clone Repository

```bash
git clone <repository-url>

cd <repository-folder>
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Backend

```bash
uvicorn models.app:app --reload --host 127.0.0.1 --port 8000
```

The FastAPI server will start on:

```
http://localhost:8000
```

---

# Run Frontend

Open another terminal and activate the virtual environment again.

```bash
streamlit run frontend.py
```

The Streamlit application will open at:

```
http://localhost:8501
```

---

# API Documentation

FastAPI automatically generates API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Docker Hub

Docker Image

https://hub.docker.com/r/nipun1a/premium-based-api

Pull Command

```bash
docker pull nipun1a/premium-based-api:latest
```

---



# Deployment

The application has been:

- Containerized using Docker
- Published on Docker Hub
- Successfully deployed on an AWS EC2 instance

---

# License

This project is intended for educational and portfolio purposes.
