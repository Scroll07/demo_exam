#!/bin/bash

echo "Starting uvicorn Fastapi"

exec uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
