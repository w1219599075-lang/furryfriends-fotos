# FurryFriends Fotos

Pet photo sharing app built with Flask and deployed on Azure.

**Live App:** https://app-furryfriends-ajhqaub7e5djdrep.uksouth-01.azurewebsites.net

---

## Prerequisites

- Azure account with active subscription
- Python 3.11
- Git
- Basic understanding of Flask and Azure

---

## Running Locally

1. Clone & install
   ```bash
   git clone https://github.com/w1219599075-lang/furryfriends-fotos.git
   cd furryfriends-fotos
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Provision PostgreSQL (any local server works). Example using `psql`:
   ```sql
   CREATE USER furry WITH PASSWORD 'furry';
   CREATE DATABASE furryfriends OWNER furry;
   \q
   ```

3. Prepare storage. Either start Azurite (`UseDevelopmentStorage=true`) or run once against your Azure account:
   ```bash
   az storage container create --name originals --connection-string "$AZURE_STORAGE_CONNECTION_STRING"
   az storage container create --name thumbnails --connection-string "$AZURE_STORAGE_CONNECTION_STRING"
   ```

4. Create `.env`
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://furry:furry@localhost:5432/furryfriends
   AZURE_STORAGE_CONNECTION_STRING=UseDevelopmentStorage=true
   AZURE_STORAGE_CONTAINER_ORIGINALS=originals
   AZURE_STORAGE_CONTAINER_THUMBNAILS=thumbnails
   ```

5. Run
   ```bash
   python app.py
   ```
   Visit http://localhost:5000

---

## Deploying to Azure

### 1. Provision resource groups
```bash
az group create -n rg-furryfriends-prod -l uksouth
az group create -n rg-furryfriends-functions -l uksouth
```

### 2. Build network boundary
- Create a VNet `vnet-furryfriends` (10.0.0.0/16) with `subnet-app` (10.0.1.0/24) and `subnet-data` (10.0.2.0/24).
- Create an NSG `nsg-app` allowing inbound 80/443 and outbound 443 only; associate it with `subnet-app`.
- Create a private endpoint for PostgreSQL into `subnet-data` so the database is reachable only inside the VNet.

### 3. Deploy core services (Portal or CLI)
- **App Service plan + Web App** in `rg-furryfriends-prod`
  ```bash
  az appservice plan create -g rg-furryfriends-prod -n plan-furryfriends -l uksouth --sku B1 --is-linux
  az webapp create -g rg-furryfriends-prod -p plan-furryfriends -n app-furryfriends -r \"PYTHON:3.11\"
  ```
- **PostgreSQL Flexible Server** (B1ms, version 14) with server parameter `require_secure_transport=On`.
- **Storage account** `stfurryfriends` (Standard LRS) plus `originals` / `thumbnails` containers.
- Enable Web App VNet integration → select `subnet-app`.

### 4. Function App for thumbnails
```bash
az functionapp create \
  -g rg-furryfriends-functions \
  -n func-furryfriends-thumb \
  --storage-account <storage-account-name> \
  --consumption-plan-location uksouth \
  --functions-version 4 \
  --runtime python
```
Deploy `functions/thumbnail_generator/` (VS Code extension, Azure CLI `func azure functionapp publish`, or zip deploy) and set the blob trigger path to monitor `originals`.

### 5. Configure App Service settings
Add the following Application Settings in App Service → Configuration:
```
SECRET_KEY=<random-string>
DATABASE_URL=postgresql://user:pass@your-server.postgres.database.azure.com/furryfriends
AZURE_STORAGE_CONNECTION_STRING=<from storage access keys>
AZURE_STORAGE_CONTAINER_ORIGINALS=originals
AZURE_STORAGE_CONTAINER_THUMBNAILS=thumbnails
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```
Function App → Configuration:
```
BUSINESS_STORAGE_CONNECTION_STRING=<same as storage above>
FUNCTIONS_WORKER_RUNTIME=python
AzureWebJobsStorage=<storage connection string>
```

### 6. Trigger deployment
- Download the publish profile from App Service → Deployment Center.
- Upload the XML content to GitHub `AZURE_WEBAPP_PUBLISH_PROFILE` secret.
- Push to `master` to let GitHub Actions deploy (details below), or run `az webapp up` for an ad-hoc deployment.

## CI/CD Pipeline
- Workflow file: `.github/workflows/main.yml`. It checks out the repo, installs dependencies with Python 3.11, and runs `azure/webapps-deploy@v2` to publish the current commit to App Service on every push to `master` (or manual dispatch).
- Required GitHub secrets:
  - `AZURE_WEBAPP_PUBLISH_PROFILE`: downloaded publish profile (XML) for `app-furryfriends`.
  - Optional extras if you extend the workflow (e.g., storage keys) but not currently consumed.
- Monitor runs via GitHub → Actions (see screenshots `18-20` under `docs/screenshots/` for reference).

---

## Environment Variables

### Web App (Flask)
| Variable | Purpose |
|----------|---------|
| SECRET_KEY | Flask session key |
| DATABASE_URL | PostgreSQL Flexible Server connection string (SSL enforced) |
| AZURE_STORAGE_CONNECTION_STRING | Storage account access |
| AZURE_STORAGE_CONTAINER_ORIGINALS | Container for original uploads |
| AZURE_STORAGE_CONTAINER_THUMBNAILS | Container for generated thumbnails |
| SCM_DO_BUILD_DURING_DEPLOYMENT | Forces App Service build on deploy (`true`) |

### Function App
| Variable | Purpose |
|----------|---------|
| BUSINESS_STORAGE_CONNECTION_STRING | Connection used by blob trigger to read/write |
| AzureWebJobsStorage | Required by Azure Functions runtime |
| FUNCTIONS_WORKER_RUNTIME | Must be `python` |

### GitHub Actions Secrets
| Secret | Purpose |
|--------|---------|
| AZURE_WEBAPP_PUBLISH_PROFILE | Allows workflow to deploy to `app-furryfriends` |

---

## Project Structure

```
furryfriends-fotos/
├── app/
│   ├── __init__.py
│   ├── models.py           # User & Image models
│   ├── routes.py           # App routes
│   ├── blob_service.py     # Storage helper
│   └── templates/
├── functions/
│   └── thumbnail_generator/
├── .github/workflows/
│   └── main.yml            # CI/CD pipeline
└── app.py
```

---

## How It Works

1. User uploads photo → stored in `originals` blob container
2. Blob trigger fires → Function generates 150x150 thumbnail
3. Thumbnail saved to `thumbnails` container
4. Image metadata saved to PostgreSQL
5. Gallery displays thumbnails for performance

---

## Troubleshooting

**App not starting?**
- Check `SCM_DO_BUILD_DURING_DEPLOYMENT=true` is set
- View logs: App Service → Log stream

**Database errors?**
- Verify connection string format
- Check Private Endpoint configuration

**Function not triggering?**
- Check Function logs
- Verify storage connection string and blob trigger setup

---

**Course Project:** HDDS2401 Cloud Services and Architectures, 2025 S1
