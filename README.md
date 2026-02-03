# 🎮 Quest Academy LMS

A **gamified Learning Management System** with RPG elements - featuring quests, battles, XP, levels, and virtual economy.

![Quest Academy LMS](https://img.shields.io/badge/Status-Active-brightgreen)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61dafb)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)

## 🚀 Features

- **Heroes (Students)**: RPG-style characters with Level, XP, HP, and Gold
- **Guild Masters (Teachers)**: Create and manage learning content
- **Worlds (Courses)**: Themed learning worlds to explore
- **Zones (Modules)**: Areas within worlds containing quests
- **Quests (Lessons)**: Learning content with XP rewards
- **Monsters (Quizzes)**: Battle monsters by answering questions
- **Assignments**: Manual tasks graded by teachers
- **Inventory & Shop**: Buy items with gold, equip for stat bonuses
- **Achievements**: Unlock trophies for accomplishments
- **Leaderboard**: Compete with other heroes globally

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, Vite, Framer Motion, React Router |
| **Backend** | FastAPI, SQLAlchemy, Alembic |
| **Database** | PostgreSQL |
| **Auth** | JWT (python-jose), Passlib |

---

## 📦 Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Magd-ayyad10/Quest-Academy-LMS.git
   cd Quest-Academy-LMS
   ```

2. **Start the database**
   ```bash
   docker-compose up -d
   ```

3. **Start the backend**
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

4. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the app**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - pgAdmin: http://localhost:5050

---

## ☁️ Deploy to Render

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Magd-ayyad10/Quest-Academy-LMS)

### Manual Deployment

#### 1. Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `quest-academy-db`
   - **Database**: `quest_academy_lms`
   - **User**: `guild_master`
   - **Plan**: Free
4. Copy the **Internal Database URL** (starts with `postgres://`)

#### 2. Deploy Backend (Web Service)

1. Click **New** → **Web Service**
2. Connect your GitHub repo
3. Configure:
   - **Name**: `quest-academy-api`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | *(paste Internal Database URL)* |
   | `SECRET_KEY` | *(generate a secure random string)* |
   | `ALGORITHM` | `HS256` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
   | `APP_NAME` | `Quest Academy LMS` |
   | `DEBUG` | `false` |

5. Click **Create Web Service**
6. Copy the deployed URL (e.g., `https://quest-academy-api.onrender.com`)

#### 3. Deploy Frontend (Static Site)

1. Click **New** → **Static Site**
2. Connect your GitHub repo
3. Configure:
   - **Name**: `quest-academy-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | `https://quest-academy-api.onrender.com` |

5. Add Rewrite Rule:
   - **Source**: `/*`
   - **Destination**: `/index.html`
   - **Type**: Rewrite

6. Click **Create Static Site**

#### 4. Run Database Migrations

After deployment, use Render Shell or run locally:
```bash
cd backend
alembic upgrade head
python scripts/seed_advanced_content.py  # Optional: seed demo data
```

---

## 📁 Project Structure

```
Quest-Academy-LMS/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routers/         # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── config.py        # Settings
│   ├── alembic/             # Database migrations
│   ├── scripts/             # Utility scripts
│   ├── main.py              # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/             # API client
│   │   ├── components/      # React components
│   │   ├── context/         # Auth context
│   │   └── pages/           # Page components
│   ├── index.html
│   └── vite.config.js
├── docker-compose.yml       # Local PostgreSQL
├── render.yaml              # Render blueprint
└── README.md
```

---

## 🔑 Default Accounts

After seeding, you can log in with:

| Role | Email | Password |
|------|-------|----------|
| Student | `hero@quest.edu` | `password123` |
| Teacher | `teacher@quest.edu` | `password123` |

---

## 📜 License

MIT License - feel free to use this project for learning and development!

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
