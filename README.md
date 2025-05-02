# Animatica-backend

***Animatica*** is my diploma project that generates videos from text and 
images using neural networks. It automates animation creation with image generation,
image-to-video conversion, and post-processing.

## Deploying on Local

### Setting up the environment

#### Step 1: Create a virtual environment

###### *Linux/macOS:*

```bash
python3 -m venv venv
source venv/bin/activate
```

###### *Windows:*

```bash
python -m venv venv
source venv/Scripts/activate
```

#### Step 2: Install requirements

```bash
cd app
pip install -r requirements.txt
```

#### Step 3: Create env files

```bash
# env/api.env

API_BASE_URL=http://localhost:8080
API_MODE=local
LOG_LEVEL=debug
FRONTEND_BASE_URL=http://localhost:8501
SESSION_SECRET_KEY=your_session_secret_key
LOCALHOST_CLIENT_ORIGIN=http://localhost:5173
ALLOWED_ORIGINS=localhost
```

```bash
# env/auth.env

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
TOKEN_ISSUER=Animatica
```

```bash
# env/db.env

DB_HOST=db
DB_PORT=5432
DB_NAME=animatica
DB_USER=postgres
DB_PASS=postgres
```

```bash
# env/ml-engine.env

ML_ENGINE_BASE_URL=http://ml-engine:90
ML_ENGINE_KEY=your-secret-key
ML_ENGINE_KEY_HEADER=X-ML-Engine-Key
```

```bash
# env/stripe.env

PUBLIC_KEY=your-public-key
SECRET_KEY=your-secret-key
```

#### Step 4: Run server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 80
```

Available endpoints:
- http://localhost:8080/docs (Swagger docs).


## Deploying via Docker

Below are the basic commands to manage docker.

###### Docker-compose

```bash
docker-compose up --build
docker-compsose down
```