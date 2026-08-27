# SpamShield - Intelligent Email Spam Detection System

An AI-powered web application that analyzes emails to detect spam using machine learning. Built with React, FastAPI, MariaDB, and scikit-learn.

## Features

- **Email Analysis**: Paste or submit emails for real-time spam classification
- **ML Classification**: TF-IDF + Multiple classifiers (Naive Bayes, Logistic Regression, Linear SVM)
- **Explainable Results**: Indicators showing why an email was classified as spam/ham
- **Dashboard**: Visual statistics with Recharts (pie charts, bar charts, trends)
- **Analysis History**: Search, filter by spam/ham, sort by date, view details, delete
- **Admin Panel**: User management, dataset management, model training & metrics
- **JWT Authentication**: Secure login with role-based access control (User / Admin)
- **Responsive UI**: Works on desktop, tablet, and mobile with dark cybersecurity theme
- **Dataset Management**: Upload CSV, add/delete training samples, label as spam/ham
- **Dataset Tooling**: CSV template download, full dataset export, source tagging (sample vs. dataset)
- **Auto-Seed & Train**: When no training data exists, seed clearly-labeled sample data and train a working model with one click
- **Model Versioning**: Track model versions, compare algorithms, view evaluation metrics
- **Role-Based Access**: Normal users cannot access admin endpoints

## Screenshots

The application features a dark cybersecurity-inspired UI with:
- Sidebar navigation
- Dashboard cards with statistics
- Recharts-powered charts (pie, bar)
- Data tables with search, filter, and pagination
- Toast notifications
- Modal dialogs
- Responsive layout

## Architecture

```
spam_detection/
├── frontend/                    # React.js + Vite application
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── Icons.jsx        # SVG icon components
│   │   │   ├── Sidebar.jsx      # Navigation sidebar
│   │   │   ├── Toast.jsx        # Toast notifications
│   │   │   ├── Modal.jsx        # Modal dialog
│   │   │   ├── ConfirmDialog.jsx
│   │   │   ├── EmptyState.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── pages/               # Page components
│   │   │   ├── LandingPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── AnalyzePage.jsx
│   │   │   ├── HistoryPage.jsx
│   │   │   ├── AnalysisDetailPage.jsx
│   │   │   ├── ProfilePage.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── UserManagement.jsx
│   │   │   ├── DatasetManagement.jsx
│   │   │   └── ModelPerformance.jsx
│   │   ├── layouts/
│   │   │   ├── Layout.jsx
│   │   │   └── AdminLayout.jsx
│   │   ├── context/
│   │   │   ├── AuthContext.jsx
│   │   │   └── ToastContext.jsx
│   │   ├── hooks/
│   │   │   └── useApi.js
│   │   ├── services/
│   │   │   └── api.js           # Axios API client
│   │   ├── utils/
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css            # Global dark theme styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── core/
│   │   │   └── config.py        # Pydantic Settings
│   │   ├── models/
│   │   │   └── models.py        # SQLAlchemy ORM models
│   │   ├── schemas/
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   ├── auth.py          # /api/auth endpoints
│   │   │   ├── users.py         # /api/users endpoints
│   │   │   ├── analysis.py      # /api/analysis endpoints
│   │   │   ├── history.py       # /api/history endpoints
│   │   │   ├── dashboard.py     # /api/dashboard endpoints
│   │   │   ├── admin.py         # /api/admin endpoints
│   │   │   ├── dataset.py       # /api/dataset endpoints
│   │   │   └── model.py         # /api/model endpoints
│   │   ├── auth/
│   │   │   └── auth.py          # JWT, password hashing
│   │   ├── database/
│   │   │   └── connection.py    # SQLAlchemy engine/session
│   │   └── utils/
│   ├── scripts/
│   │   ├── init_db.py           # DB init + admin creation
│   │   ├── seed_data.py         # Seed sample training data
│   │   └── evaluate_model.py    # Model evaluation script
│   ├── tests/
│   │   ├── test_api.py          # API unit tests
│   │   └── test_ml.py           # ML module unit tests
│   ├── run.py                   # Direct uvicorn runner
│   └── requirements.txt
├── ml/                          # Machine Learning module
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── dataset/
│   │   └── loader.py            # CSV loading & validation
│   ├── preprocessing/
│   │   └── text_cleaner.py      # Text cleaning pipeline
│   ├── training/
│   │   └── trainer.py           # Multi-model training
│   ├── models/
│   │   ├── model_manager.py     # Save/load model versions
│   │   └── saved/               # Trained model artifacts
│   ├── evaluation/
│   │   └── evaluator.py         # Accuracy, precision, recall, F1
│   ├── prediction/
│   │   ├── predictor.py         # Prediction engine
│   │   └── explainer.py         # Explainable indicators
│   └── utils/
│       └── config.py            # ML constants
├── .gitignore
├── .env.example
└── README.md
```

## Technologies

| Layer       | Technology                                                          |
|-------------|---------------------------------------------------------------------|
| Frontend    | React 18, Vite, Recharts, Axios, React Router 6                    |
| Backend     | Python 3.10+, FastAPI, SQLAlchemy, Pydantic v2, Pydantic Settings  |
| Database    | MariaDB (via PyMySQL driver)                                        |
| ML/AI       | scikit-learn, pandas, numpy, nltk, joblib                           |
| Auth        | JWT (python-jose), bcrypt (passlib)                                 |
| Testing     | pytest, pytest-asyncio                                              |

## ML Pipeline

### Text Preprocessing
1. Lowercase conversion
2. HTML tag removal
3. URL removal (replaced with `URL` token)
4. Email address removal (replaced with `EMAIL` token)
5. Phone number removal
6. Number removal
7. Punctuation removal
8. Tokenization
9. Stop word removal (English)
10. Optional lemmatization

### Feature Extraction
- TF-IDF Vectorization
- Max features: 5,000
- N-gram range: (1, 2)
- Min document frequency: 2
- Max document frequency: 0.95
- Sublinear TF scaling

### Classifiers Compared
- **Multinomial Naive Bayes** - Fast, good baseline
- **Logistic Regression** - Strong linear classifier
- **Linear SVM** (CalibratedClassifierCV) - Best for text classification

The best model is selected based on F1 score and saved automatically.

### Explainable Detection Indicators
For each prediction, the system checks for:
- Excessive capitalization (>30% uppercase)
- Spam-related keywords (free, winner, click, claim, etc.)
- Multiple URLs/links
- Sensitive information requests (password, credit card, SSN)
- Urgency language (act now, limited time, expires)
- Promotional language (discount, offer, deal)
- Suspicious sender patterns (no-reply)
- Monetary amounts
- Excessive punctuation (!!!, ???)

## Database Schema

### Users Table
| Column        | Type         | Description                    |
|---------------|--------------|--------------------------------|
| id            | INT (PK)     | Auto-increment ID              |
| name          | VARCHAR(255) | User's full name               |
| email         | VARCHAR(255) | Unique email address           |
| password_hash | VARCHAR(255) | Bcrypt hashed password         |
| role          | VARCHAR(20)  | "user" or "admin"              |
| created_at    | DATETIME     | Account creation timestamp     |

### Email Analyses Table
| Column        | Type         | Description                    |
|---------------|--------------|--------------------------------|
| id            | INT (PK)     | Auto-increment ID              |
| user_id       | INT (FK)     | References users.id            |
| sender        | VARCHAR(255) | Sender email address           |
| subject       | VARCHAR(500) | Email subject line             |
| body          | TEXT         | Full email body                |
| prediction    | VARCHAR(10)  | "spam" or "ham"                |
| confidence    | FLOAT        | Confidence score (0-100)       |
| risk_level    | VARCHAR(20)  | "high", "medium", or "low"     |
| indicators    | TEXT (JSON)   | JSON array of indicators       |
| model_version | VARCHAR(50)  | ML model version used          |
| created_at    | DATETIME     | Analysis timestamp             |

### Training Samples Table
| Column     | Type     | Description                     |
|------------|----------|---------------------------------|
| id         | INT (PK) | Auto-increment ID               |
| message    | TEXT     | Email text content              |
| label      | VARCHAR  | "spam" or "ham"                 |
| source     | VARCHAR  | "sample" (built-in/dev) or "dataset" (uploaded) |
| created_at | DATETIME | Sample creation timestamp       |

### Model Versions Table
| Column     | Type     | Description                     |
|------------|----------|---------------------------------|
| id         | INT (PK) | Auto-increment ID               |
| version    | VARCHAR  | Version string (e.g., "v1")     |
| algorithm  | VARCHAR  | Classifier name                 |
| accuracy   | FLOAT    | Test accuracy                   |
| precision  | FLOAT    | Test precision                  |
| recall     | FLOAT    | Test recall                     |
| f1_score   | FLOAT    | Test F1 score                   |
| trained_at | DATETIME | Training timestamp              |

## Database Setup

### 1. Install MariaDB

```bash
# macOS
brew install mariadb
brew services start mariadb

# Ubuntu/Debian
sudo apt install mariadb-server
sudo systemctl start mariadb

# Windows - Download from https://mariadb.org/download/
```

### 2. Create Database

```sql
CREATE DATABASE spam_detection CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your MariaDB credentials
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

### 2. Option A: Train via CLI

```bash
cd ml
python main.py train /path/to/dataset.csv
```

### 3. Option B: Train via Admin UI

1. Start the backend server
2. Login as admin
3. Upload training samples via Dataset Management, OR if you have no dataset yet, click **"Seed Sample Data"** (loads clearly-labeled development samples) or **"Seed Sample Data & Train"** on the Model Performance page
4. Navigate to Model Performance
5. Click "Train/Retrain Model"

> **Note on sample data:** The built-in sample emails are clearly labeled as development data for demonstration/testing only. For production use, upload a real labeled dataset (via Dataset Management > Upload CSV, using the downloadable template format).

### 4. Evaluate the Model

```bash
cd backend
python -m scripts.evaluate_model /path/to/dataset.csv
```

### Dataset Tools (Admin)

- **Download Template** — get a `template.csv` showing the expected `label,message` format
- **Export Dataset** — download all training samples as `training_dataset.csv`
- **Source Tagging** — each sample is tagged `sample` (built-in/dev) or `dataset` (uploaded) so you can tell them apart

### Dataset Format

Upload CSV files with these columns:

```csv
label,message
spam,"FREE iPhone! Click here to claim your prize now!"
ham,"Hi, meeting tomorrow at 10am. Let me know if available."
```

Supported label formats: `spam`/`ham`, `1`/`0`, `true`/`false`

## Environment Variables

Create `backend/.env` from `backend/.env.example`:

| Variable                          | Description                       | Default                              |
|-----------------------------------|-----------------------------------|--------------------------------------|
| `DB_HOST`                         | MariaDB host                      | `localhost`                          |
| `DB_PORT`                         | MariaDB port                      | `3306`                               |
| `DB_USER`                         | MariaDB user                      | `root`                               |
| `DB_PASSWORD`                     | MariaDB password                  | (required)                           |
| `DB_NAME`                         | Database name                     | `spam_detection`                     |
| `JWT_SECRET_KEY`                  | JWT signing secret                | (change in production)               |
| `JWT_ALGORITHM`                   | JWT algorithm                     | `HS256`                              |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes           | `60`                                 |
| `CORS_ORIGINS`                    | Allowed origins (JSON array)      | `["http://localhost:3000"]`          |
| `DEBUG`                           | Enable debug mode                 | `true`                               |
| `HOST`                            | Server host                       | `0.0.0.0`                           |
| `PORT`                            | Server port                       | `8000`                               |

## Installation & Running

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m scripts.init_db --admin-email admin@spamdetect.com --admin-password admin123 --create-test-user
python -m scripts.seed_data          # Optional: seed 40 sample training records
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

## API Documentation

Once the backend is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Authentication Endpoints

| Method | Endpoint              | Description         | Auth   |
|--------|-----------------------|---------------------|--------|
| POST   | `/api/auth/register`  | Register new user   | Public |
| POST   | `/api/auth/login`     | Login               | Public |

### User Endpoints

| Method | Endpoint              | Description         | Auth   |
|--------|-----------------------|---------------------|--------|
| GET    | `/api/users/me`       | Get profile         | User   |
| GET    | `/api/users/me/stats` | Personal analysis stats | User |
| PUT    | `/api/users/me`       | Update profile      | User   |
| PUT    | `/api/users/me/password` | Change password  | User   |

### Analysis Endpoints

| Method | Endpoint              | Description         | Auth   |
|--------|-----------------------|---------------------|--------|
| POST   | `/api/analysis/`      | Analyze an email    | User   |
| GET    | `/api/analysis/`      | List my analyses    | User   |
| GET    | `/api/analysis/{id}`  | Get analysis detail | User   |
| DELETE | `/api/analysis/{id}`  | Delete analysis     | User   |

### History & Dashboard Endpoints

| Method | Endpoint              | Description         | Auth   |
|--------|-----------------------|---------------------|--------|
| GET    | `/api/history/`       | Get analysis history| User   |
| GET    | `/api/history/dashboard` | User dashboard  | User   |
| GET    | `/api/dashboard/`     | Dashboard stats     | User   |

### Admin Endpoints

| Method | Endpoint                  | Description             | Auth  |
|--------|---------------------------|-------------------------|-------|
| GET    | `/api/admin/stats`        | System statistics       | Admin |
| GET    | `/api/admin/users`        | List all users          | Admin |
| DELETE | `/api/admin/users/{id}`   | Delete user             | Admin |
| GET    | `/api/admin/analyses`     | List all analyses       | Admin |
| DELETE | `/api/admin/analyses/{id}`| Delete analysis         | Admin |
| GET    | `/api/admin/model-versions`| Model version history  | Admin |

### Dataset Endpoints (Admin Only)

| Method | Endpoint                  | Description             | Auth  |
|--------|---------------------------|-------------------------|-------|
| GET    | `/api/dataset/`           | List training samples   | Admin |
| GET    | `/api/dataset/stats`      | Dataset statistics      | Admin |
| GET    | `/api/dataset/template`   | Download CSV template   | Admin |
| GET    | `/api/dataset/export`     | Export all samples as CSV | Admin |
| POST   | `/api/dataset/`           | Add training sample     | Admin |
| POST   | `/api/dataset/upload`     | Upload CSV dataset      | Admin |
| POST   | `/api/dataset/bulk`       | Bulk add samples        | Admin |
| DELETE | `/api/dataset/{id}`       | Delete sample           | Admin |
| DELETE | `/api/dataset/clear-all`  | Delete all samples      | Admin |

### Model Endpoints (Admin Only)

| Method | Endpoint                  | Description             | Auth  |
|--------|---------------------------|-------------------------|-------|
| GET    | `/api/model/versions`     | List model versions     | Admin |
| GET    | `/api/model/current`      | Current model info      | Admin |
| GET    | `/api/model/dataset-status`| Dataset trainability   | Admin |
| POST   | `/api/model/train`        | Train/retrain model     | Admin |
| POST   | `/api/model/seed-sample-data` | Load built-in sample dataset | Admin |
| POST   | `/api/model/seed-and-train`  | Seed sample data & train | Admin |

## Testing

```bash
cd backend
python -m pytest tests/ -v
```

### Test Coverage

- API endpoint validation tests
- ML text preprocessing tests
- Explainer indicator tests
- Dataset loader validation tests
- Model manager registry tests

## Default Accounts

| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| Admin | admin@spamdetect.com     | admin123  |
| User  | test@test.com            | test123   |

## Security

- Passwords hashed with bcrypt (never stored in plain text)
- JWT-based authentication with configurable expiry
- Role-based access control (User / Admin)
- Input validation via Pydantic schemas
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for allowed origins
- Environment variables for secrets (no hardcoded credentials)
- Dataset upload validation (file type, size, format)
- Maximum email input size limit (50,000 characters)

## License

This project is for educational and portfolio purposes.
