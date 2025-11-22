project-root/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Settings (Pydantic BaseSettings)
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py                # Dependency injection
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py          # Main API router
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py
│   │   │           ├── users.py
│   │   │           └── items.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py            # Auth, hashing, JWT
│   │   │   ├── cache.py               # Redis client
│   │   │   └── websocket.py           # WebSocket manager
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # SQLAlchemy Base
│   │   │   ├── session.py             # DB session
│   │   │   └── init_db.py             # DB initialization
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── item.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # Pydantic schemas
│   │   │   └── item.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # Business logic
│   │   │   └── item.py
│   │   │
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py          # Celery/Dramatiq config
│   │   │   └── background.py          # Background tasks
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py              # Logging setup
│   │       └── helpers.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_utils/
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml                 # Black, Ruff, mypy config
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/ nothing in, dont wanna do it right now
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   ├── loki/
│   │   └── loki-config.yml
│   └── promtail/
│       └── promtail-config.yml
│
├── docker-compose.yml                 # Dev environment
├── docker-compose.prod.yml            # Production setup
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── k8s/                               # Kubernetes manifests
│   ├── backend/
│   ├── frontend/
│   └── monitoring/
│
├── .gitignore
├── README.md
├── LICENSE
└── Makefile                           # Common commands