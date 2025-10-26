# PROCON 2025

## 🧱 1. Cấu trúc dự án
```lua
procon2025/
├── app/
│   ├── core/              # Cấu hình hệ thống (config, db, security, auth)
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── auth.py
│   ├── models/            # ORM models
│   │   └── models.py
│   ├── schemas/           # Pydantic schemas
│   │   ├── user.py
│   │   ├── problem.py
│   │   └── submission.py
│   ├── api/               # API routes (modular)
│   │   ├── routes_user.py
│   │   ├── routes_submit.py
│   │   └── routes_auth.py
│   ├── services/          # Logic xử lý (judge, validate, ranking,...)
│   │   └── judge.py
│   ├── utils/             # Hàm tiện ích
│   └── main.py            # Entry point FastAPI
├── logs/
├── storages/
├── Dockerfile
├── compose.yml
├── requirements.txt
└── alembic/               # DB migration (alembic)
```

## 🛠️ 2. Công nghệ sử dụng
| Thành phần | Công nghệ                |
| ---------- | ------------------------ |
| API        | FastAPI                  |
| DB         | PostgreSQL               |
| ORM        | SQLAlchemy 2.0 + Alembic |
| Auth       | OAuth2 với JWT           |
| Đồng thời  | `asyncio.Semaphore`      |
| Container  | Docker + docker-compose  |

## 3. Hướng dẫn khởi động nhanh

```bash
docker compose build
docker compose up -d
```

API: `http://localhost:8000`
Web ranking: `http://localhost:8001/rank/user`
Web simulatate (demo): `http://localhost:8080/simulation`

