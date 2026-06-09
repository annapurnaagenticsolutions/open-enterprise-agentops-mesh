FROM python:3.12-slim

WORKDIR /app

COPY framework/backend/pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir "fastapi>=0.110.0" "uvicorn[standard]>=0.27.0" "pydantic>=2.6.0"

COPY framework/backend/agentops_mesh_api /app/agentops_mesh_api
COPY framework/backend/data /app/data
COPY deployment /app/deployment
COPY platform /app/platform
COPY release /app/release
COPY benchmarks /app/benchmarks

EXPOSE 8080
CMD ["uvicorn", "agentops_mesh_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
