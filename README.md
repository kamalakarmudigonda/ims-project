# IMS (Incident Management System)

## 📌 Overview
This project is a simple Incident Management System built using FastAPI.  
It helps in detecting, grouping, and resolving incidents efficiently.

---

## 🚀 Features
- Receive signals from systems
- Group signals into incidents
- Auto-create incidents
- Close incidents with RCA (Root Cause Analysis)
- Calculate MTTR (Mean Time to Resolution)

---

## 🔗 API Endpoints
- `GET /` → Check service status  
- `POST /signal` → Send signal  
- `GET /incidents` → Get all incidents  
- `POST /close/{id}` → Close incident  

---

## 🛠️ Tech Stack
- FastAPI  
- Python  
- Docker  
- AWS EC2  

---

## ▶️ How to Run

```bash
docker-compose up --build

http://32.192.215.79:8000/docs


