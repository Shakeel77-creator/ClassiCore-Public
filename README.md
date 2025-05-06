
---

# 🚀 ClassiCore – AI-Powered UNSPSC Classifier

ClassiCore is an enterprise-ready tool that intelligently classifies product/service descriptions into accurate **UNSPSC codes** using advanced **semantic search** and **AI inference**.

---

## 📌 Table of Contents

* [System Architecture](#system-architecture)
* [Tech Stack](#tech-stack)
* [Deployment Prerequisites](#deployment-prerequisites)
* [Step-by-Step Deployment on AWS EC2 (g5 GPU)](#step-by-step-deployment-on-aws-ec2-g5-gpu)
* [Running the Application](#running-the-application)
* [Directory Structure](#directory-structure)
* [API Contract](#api-contract)
* [Contributors](#contributors)

---

## 🏗️ System Architecture

```
                        ┌────────────────────┐
                        │   React Frontend   │
                        └────────┬───────────┘
                                 │
                                 ▼
                        ┌────────────────────┐
                        │  Spring Boot API   │
                        └────────┬───────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  FastAPI AI Classifier   │
                    └────────┬───────────┬─────┘
                             │           │
              ┌──────────────┘           └───────────────┐
              ▼                                          ▼
       SQLite (UNSPSC Data)                  SentenceTransformer (Embeddings)
```

---

## 💻 Tech Stack

| Layer         | Technology                                  |
| ------------- | ------------------------------------------- |
| Frontend      | React.js, Vite, Tailwind                    |
| Backend API   | Spring Boot (Java)                          |
| AI Service    | FastAPI (Python), Hugging Face Transformers |
| Model Hosting | Mistral / IBM Granite                       |
| Embeddings    | SentenceTransformers (all-MiniLM)           |
| DB            | SQLite (embedded UNSPSC dataset)            |
| Infra         | AWS EC2 g5.xlarge (with GPU), Docker        |
| Logging       | Console + future plan for ELK/CloudWatch    |

---

## ⚙️ Deployment Prerequisites

1. **AWS EC2 g5.xlarge instance** (Ubuntu 22.04)

2. **Security Group:**

   * Port 3000 (Frontend)
   * Port 8080 (Spring Boot Backend)
   * Port 8000 (Python FastAPI)

3. **Install Docker**

4. **Install NVIDIA GPU drivers:**

   ```bash
   sudo apt update && sudo apt upgrade
   sudo apt install nvidia-driver-525
   reboot
   ```

5. **Install NVIDIA Container Toolkit:**

   ```bash
   sudo apt install nvidia-container-toolkit
   sudo systemctl restart docker
   ```

6. **Test GPU with Docker:**

   ```bash
   docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
   ```

---

## 🚀 Step-by-Step Deployment on AWS EC2 (g5 GPU)

### 1. Clone Project

```bash
git clone https://github.com/your-org/classicore.git
cd classicore
```

### 2. Build and Run with Docker Compose

```bash
docker compose --profile prod up --build -d
```

> This spins up all 3 services: `frontend`, `backend (Spring Boot)`, and `ai-classifier (FastAPI)` with GPU access enabled.

### 3. Check Logs

```bash
docker logs classicore-backend
docker logs classicore-classifier
docker logs classicore-frontend
```

---

## 🖥️ Running the Application

* Access Frontend: `http://<EC2-IP>:3000`
* API (optional): `http://<EC2-IP>:8080`
* AI Classifier: `http://<EC2-IP>:8000`

---

## 📁 Directory Structure

```
classicore/
├── frontend/              # React.js UI
├── backend/               # Spring Boot API
├── ai-classifier/         # Python FastAPI + Embeddings
├── unspsc.sqlite          # Classification DB (auto-mounted)
├── docker-compose.yml     # Multi-container setup with GPU
├── README.md              # This file
```

---

## 📨 API Contract

### POST `/classify`

```json
{
  "product_name": "medical face mask"
}
```

### Response:

```json
[
  {
    "code": "42131728",
    "label": "Antifog surgical masks and tie back masks",
    "confidence": 66.7,
    "source": "Semantic Search"
  },
  ...
]
```

---

## 👨‍💻 Contributors

* **Shakeel** – Architect & Full Stack Developer

---
