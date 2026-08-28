# Quick Start

## Prerequisites
- Python 3.12+
- MariaDB running on port 3306
- Node.js 20+

## 1. Setup Database
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS spam_detection CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## 2. Backend
```bash
cd backend
cp .env.example .env  # Edit with your DB credentials
pip install -r requirements.txt
python -m backend.scripts.init_db --admin-email admin@spamdetect.com --admin-password admin123 --create-test-user
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8001
```

## 3. Seed Dataset & Train Model
```bash
# Via API (admin login required):
curl -X POST http://localhost:8001/api/auth/login -H "Content-Type: application/json" -d '{"email":"admin@spamdetect.com","password":"admin123"}'
# Use the returned token to call:
curl -X POST http://localhost:8001/api/model/seed-and-train -H "Authorization: Bearer <token>"
```

## 4. Frontend
```bash
cd frontend
npm install
npm run dev
```

## 5. Open
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## Default Accounts
| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| Admin | admin@spamdetect.com     | admin123  |
| User  | test@test.com            | test123   |
