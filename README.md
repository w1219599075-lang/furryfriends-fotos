# FurryFriends Fotos

A simple pet photo sharing web app built with Flask and deployed on Azure.

## About This Project

This is a course project for HDDS2401 Cloud Services and Architectures. It's basically a social platform where users can upload photos of their pets and view other people's pet photos. The main focus is on cloud deployment and architecture design.

## What It Does

- Users can register and login
- Upload pet photos
- Automatically generates thumbnails for each photo
- Browse all photos in a public gallery

## Tech Stack

Backend:
- Python 3.11 + Flask
- PostgreSQL database
- SQLAlchemy for database stuff

Frontend:
- Bootstrap for styling
- Jinja2 templates

Azure Services:
- App Service (hosting the web app)
- PostgreSQL (database)
- Blob Storage (storing images)
- Functions (auto thumbnail generation)
- VNet and NSG (network security)

CI/CD:
- GitHub Actions for automatic deployment

## Setup Instructions

### Running Locally

1. Clone the repo
```bash
git clone https://github.com/w1219599075-lang/furryfriends-fotos.git
cd furryfriends-fotos
```

2. Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# then edit .env with your Azure credentials
```

4. Run the app
```bash
python app.py
```

Visit http://localhost:5000 to see it running.

### Deploying to Azure

The deployment is automated through GitHub Actions. Just push to the master branch and it will automatically deploy to Azure App Service.

You'll need to configure:
- Azure App Service
- PostgreSQL database
- Blob Storage account
- Azure Function for thumbnails
- GitHub secrets for deployment


## Course Info

- Course: HDDS2401 Cloud Services and Architectures
- Semester: 2025 S1

