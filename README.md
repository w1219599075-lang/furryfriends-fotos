# FurryFriends Fotos

A simple pet photo sharing web app built with Flask and deployed on Azure.

## About

This is a course project for HDDS2401 Cloud Services and Architectures (2025 S1). It's basically a social platform where users can upload photos of their pets and view other people's pet photos. The main focus is on cloud deployment and architecture design.

**Key Features:**
- User registration and login
- Upload pet photos (stored in Azure Blob Storage)
- Automatic thumbnail generation (via Azure Functions)
- Public gallery to browse all photos

**Tech Stack:**
- Backend: Python 3.11, Flask, SQLAlchemy, PostgreSQL
- Frontend: Bootstrap 5, Jinja2 templates
- Cloud: Azure App Service, PostgreSQL, Blob Storage, Functions, VNet, NSG
- CI/CD: GitHub Actions

**Live Demo:** (will be added after deployment)

---

## Prerequisites

Before you start, make sure you have:

- Python 3.11 or higher
- Git
- An Azure account with an active subscription
- Azure CLI installed (for deployment)
- A GitHub account

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/w1219599075-lang/furryfriends-fotos.git
cd furryfriends-fotos
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example env file and edit it with your settings:

```bash
cp .env.example .env
```

Then edit `.env` file with your configuration (see Environment Variables section below).

### 5. Run Locally

For local development, you can use SQLite instead of PostgreSQL:

```bash
python app.py
```

The app will be available at `http://localhost:5000`

**Note:** Some features like Azure Blob Storage upload and thumbnail generation won't work locally unless you configure Azure credentials in `.env`.

---

## Environment Variables

Create a `.env` file in the project root with these variables:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_APP=app.py
FLASK_ENV=development

# Database (use SQLite for local, PostgreSQL for production)
DATABASE_URL=postgresql://username:password@host:5432/dbname

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_STORAGE_CONTAINER_ORIGINAL=originals
AZURE_STORAGE_CONTAINER_THUMBNAIL=thumbnails

# Azure Storage Account (alternative to connection string)
AZURE_STORAGE_ACCOUNT_NAME=your-account-name
AZURE_STORAGE_ACCOUNT_KEY=your-account-key
```

**Important:** Never commit `.env` file to Git. It's already in `.gitignore`.

---

## Manual Deployment to Azure

### Step 1: Create Azure Resources

You'll need to create these Azure resources (detailed steps to be added):

1. **Resource Group**
   - Name: `furryfriends-rg`
   - Region: East Asia (or your preferred region)

2. **App Service**
   - Plan: B1 (Basic)
   - Runtime: Python 3.11

3. **PostgreSQL Database**
   - SKU: Burstable B1ms
   - Create database named `furryfriends`

4. **Blob Storage Account**
   - Create two containers: `originals` and `thumbnails`
   - Set container access level to Blob

5. **Azure Function**
   - Runtime: Python 3.11
   - Plan: Consumption
   - Add Blob trigger for thumbnail generation

6. **Virtual Network & NSG**
   - Create VNet with subnets for app and database
   - Configure NSG rules for security

### Step 2: Configure App Service

(Detailed configuration steps will be added after testing)

1. Set environment variables in App Service Configuration
2. Configure deployment source
3. Enable VNet integration

### Step 3: Deploy Application

**Option 1: Using GitHub Actions (Automated)**

The repo includes a GitHub Actions workflow that automatically deploys when you push to master branch. You need to configure these GitHub Secrets:

- `AZURE_WEBAPP_PUBLISH_PROFILE`
- Other secrets (to be documented)

**Option 2: Manual Deployment via Azure CLI**

```bash
# Login to Azure
az login

# Deploy to App Service
az webapp up --name your-app-name --resource-group furryfriends-rg
```

(More detailed steps will be added)

### Step 4: Deploy Azure Function

(Steps for deploying the thumbnail generation function will be added)

---

## Project Structure

```
furryfriends-fotos/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # Route handlers
│   ├── forms.py             # WTForms
│   ├── config.py            # Configuration
│   ├── blob_service.py      # Azure Blob operations
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── functions/
│   └── thumbnail_generator/ # Azure Function code
├── .github/
│   └── workflows/           # GitHub Actions
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore
├── app.py                   # Application entry point
└── README.md
```

---

## Testing the Application

After deployment, test these features:

1. Register a new user account
2. Login with the account
3. Upload a pet photo
4. Check if thumbnail is auto-generated (wait ~10 seconds)
5. View the gallery page
6. Logout

---

## Troubleshooting

**App won't start locally:**
- Check if virtual environment is activated
- Make sure all dependencies are installed
- Check Python version (needs 3.11+)

**Can't upload images:**
- Verify Azure Storage credentials in `.env`
- Check if containers exist in Blob Storage

**Database connection error:**
- For local dev, remove `DATABASE_URL` from `.env` to use SQLite
- For production, verify PostgreSQL connection string

---

## Course Information

- **Course:** HDDS2401 Cloud Services and Architectures
- **Semester:** 2025 S1
- **Assignment:** Group Project (40% of final grade)
- **GitHub:** https://github.com/w1219599075-lang/furryfriends-fotos
