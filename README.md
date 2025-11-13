# FurryFriends Fotos

A pet photo sharing social platform built on Microsoft Azure.

## 🎯 Project Overview

FurryFriends Fotos is a cloud-based web application that allows users to share photos of their pets. This project demonstrates cloud architecture design and deployment skills using Azure services.

## 🏗️ Architecture

- **Hosting**: Azure App Service (PaaS)
- **Database**: Azure Database for PostgreSQL
- **Storage**: Azure Blob Storage (originals + thumbnails)
- **Functions**: Azure Functions (thumbnail generation)
- **Network**: Azure Virtual Network with NSG
- **CI/CD**: GitHub Actions

## 🚀 Features

- User registration and authentication
- Photo upload with automatic thumbnail generation
- Public photo gallery
- Secure cloud storage

## 💻 Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0
- SQLAlchemy
- Flask-Login

**Frontend:**
- Bootstrap 5
- Jinja2 Templates

**Cloud Services:**
- Azure App Service
- Azure PostgreSQL
- Azure Blob Storage
- Azure Functions
- Azure VNet & NSG

## 📦 Installation

### Prerequisites
- Python 3.11+
- Azure Account
- Git

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd furryfriends-fotos
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python app.py
```

6. Access at `http://localhost:5000`

## 🌐 Deployment

The application is automatically deployed to Azure App Service via GitHub Actions when code is pushed to the main branch.

## 📝 License

This project is created for HDDS2401 Cloud Services and Architectures course assignment.

## 👥 Author

- Student ID: [Your ID]
- Course: HDDS2401 Cloud Services and Architectures
- Semester: 2025 S1
