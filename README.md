# SpamShield - Intelligent Email Spam Detection System

An AI-powered web application that analyzes emails to detect spam using machine learning. Built with React, FastAPI, MariaDB, and scikit-learn.

## Features

- **Email Analysis**: Paste or submit emails for real-time spam classification
- **ML Classification**: TF-IDF + Multiple classifiers (Naive Bayes, Logistic Regression, SVM)
- **Explainable Results**: Indicators showing why an email was classified as spam/ham
- **Dashboard**: Visual statistics with charts and analysis trends
- **Analysis History**: Search, filter, sort, and manage past analyses
- **Admin Panel**: User management, dataset management, model training
- **JWT Authentication**: Secure login with role-based access control
- **Responsive UI**: Works on desktop, tablet, and mobile

## Architecture

```
spam_detection/
├── frontend/          # React.js application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── layouts/       # Layout wrappers
│   │   ├── context/       # React context (Auth, Toast)
│   │   ├── services/      # API service (Axios)
│   │   └── index.css      # Global styles
│   └── package.json
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── core/          # Configuration
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # API route handlers
│   │   ├── auth/          # JWT authentication
│   │   ├── database/      # DB connection
│   │   └── utils/         # Utilities
│   ├── scripts/           # DB init, seed, eval scripts
│   ├── tests/             # Unit tests
│   └── requirements.txt
├── ml/                # Machine Learning module
│   ├── dataset/           # Dataset loading & validation
│   ├── preprocessing/     # Text cleaning pipeline
│   ├── training/          # Model training
│   ├── models/            # Model persistence & versioning
│   ├── evaluation/        # Metrics computation
│   ├── prediction/        # Prediction & explainability
│   ├── utils/             # ML configuration
│   └── main.py            # CLI entry point
└── README.md
```

## Technologies

| Layer       | Technology                                          |
|-------------|-----------------------------------------------------|
| Frontend    | React 18, Vite, Recharts, Axios, React Router 6    |
| Backend     | Python, FastAPI, SQLAlchemy, Pydantic               |
| Database    | MariaDB (via PyMySQL)                               |
| ML/AI       | scikit-learn, pandas, numpy, nltk                   |
| Auth        | JWT (python-jose), bcrypt (passlib)                 |

## Database Setup

### 1. Install MariaDB

```bash
# macOS
brew install mariadb
brew services start mariadb

# Ubuntu/Debian
sudo apt install mariadb-server
sudo systemctl start mariadb
```

### 2. Create Database

```sql
CREATE DATABASE spam_detection CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Initialize Database & Create Admin

```bash
cd backend
python -m scripts.init_db --admin-email admin@spamdetect.com --admin-password admin123 --create-test-user
```

## ML Setup

### 1. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Train the Model

Option A - Via CLI:
```bash
cd ml
python main.py train /path/to/dataset.csv
```

Option B - Via API (admin only):
- Start the backend
- Login as admin
- Upload training samples via Dataset Management
- Click "Train/Retrain Model" on the Model Performance page

### 3. Evaluate the Model

```bash
cd backend
python scripts/evaluate_model.py /path/to/dataset.csv
```

## Environment Variables

Create `backend/.env` from `backend/.env.example`:

| Variable                     | Description                         | Default                          |
|------------------------------|-------------------------------------|----------------------------------|
| `DB_HOST`                    | MariaDB host                        | `localhost`                      |
| `DB_PORT`                    | MariaDB port                        | `3306`                           |
| `DB_USER`                    | MariaDB user                        | `root`                           |
| `DB_PASSWORD`                | MariaDB password                    | (required)                       |
| `DB_NAME`                    | Database name                       | `spam_detection`                 |
| `JWT_SECRET_KEY`             | JWT signing key                     | (change in production)           |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry minutes          | `30`                             |
| `CORS_ORIGINS`               | Allowed CORS origins (JSON array)   | `["http://localhost:3000"]`      |

## Installation & Running

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m scripts.init_db --admin-email admin@spamdetect.com --admin-password admin123 --create-test-user
python -m scripts.seed_data  # Optional: seed sample training data
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000

### Training the Model

```bash
# Via CLI with a CSV dataset
cd ml
python main.py train /path/to/spam_dataset.csv

# Or upload CSV via the admin UI and train from there
```

## API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint                | Description              | Auth     |
|--------|-------------------------|--------------------------|----------|
| POST   | `/api/auth/register`    | Register new user        | Public   |
| POST   | `/api/auth/login`       | Login                    | Public   |
| GET    | `/api/users/me`         | Get profile              | User     |
| PUT    | `/api/users/me`         | Update profile           | User     |
| POST   | `/api/analysis/`        | Analyze an email         | User     |
| GET    | `/api/analysis/`        | List my analyses         | User     |
| GET    | `/api/analysis/{id}`    | Get analysis details     | User     |
| DELETE | `/api/analysis/{id}`    | Delete analysis          | User     |
| GET    | `/api/history/`         | Get analysis history     | User     |
| GET    | `/api/history/dashboard`| Dashboard statistics     | User     |
| GET    | `/api/dashboard/`       | Dashboard statistics     | User     |
| GET    | `/api/admin/stats`      | Admin system stats       | Admin    |
| GET    | `/api/admin/users`      | List all users           | Admin    |
| DELETE | `/api/admin/users/{id}` | Delete user              | Admin    |
| GET    | `/api/admin/analyses`   | List all analyses        | Admin    |
| POST   | `/api/dataset/`         | Add training sample      | Admin    |
| POST   | `/api/dataset/upload`   | Upload CSV dataset       | Admin    |
| POST   | `/api/model/train`      | Train/retrain model      | Admin    |
| GET    | `/api/model/versions`   | List model versions      | Admin    |

## Testing

```bash
cd backend
python -m pytest tests/ -v
```

## Default Accounts

| Role  | Email                    | Password |
|-------|--------------------------|----------|
| Admin | admin@spamdetect.com     | admin123 |
| User  | test@test.com            | test123  |

## License

This project is for educational purposes.
