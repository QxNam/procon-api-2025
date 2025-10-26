#!/bin/bash

export MODE="DEV"
export POSTGRES_URL="postgresql+asyncpg://admin:admin@localhost:5432/procondb"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
