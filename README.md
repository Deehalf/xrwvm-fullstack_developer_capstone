# fullstack_developer_capstone

https://github.com/Deehalf/xrwvm-fullstack_developer_capstone/

# Dealership Reviews Platform

Plataforma full‑stack para la gestión de concesionarios y reseñas de autos, desarrollada como parte del proyecto final del programa IBM Full Stack Developer.  
Incluye backend en **Django**, microservicio en **Node.js + MongoDB**, y frontend en **React**.

---

## 🚀 Arquitectura del Proyecto

El sistema está compuesto por tres módulos principales:

### 1. **Backend Django (API Gateway)**
- Maneja autenticación de usuarios.
- Expone endpoints REST para:
  - Login / Logout / Registro
  - Obtener concesionarios
  - Obtener reseñas
  - Enviar reseñas al microservicio Node
- Procesa análisis de sentimiento mediante un servicio externo.

### 2. **Microservicio Node.js + MongoDB**
- Almacena concesionarios y reseñas.
- Expone endpoints REST:
  - `/fetchDealers`
  - `/fetchDealers/:state`
  - `/fetchDealer/:id`
  - `/fetchReviews`
  - `/fetchReviews/dealer/:id`
  - `/insert_review`
- Inicializa la base de datos con datos JSON.

### 3. **Frontend React**
- Interfaz para:
  - Ver concesionarios
  - Ver reseñas
  - Agregar reseñas
  - Autenticación de usuarios

---

## 🛠️ Tecnologías Utilizadas

### Backend Django
- Python 3.12
- Django 3.2
- Django REST Framework
- SQLite (solo para usuarios)
- Requests

### Microservicio Node
- Node.js 18+
- Express.js
- Mongoose
- MongoDB
- CORS
- Body‑Parser

### Frontend
- React
- Fetch API
- Bootstrap

### DevOps / CI
- GitHub Actions
- Flake8 (linting Python)
- JSHint (linting JavaScript)
- Docker (entorno de ejecución en Theia)

---

## 📂 Estructura del Proyecto

