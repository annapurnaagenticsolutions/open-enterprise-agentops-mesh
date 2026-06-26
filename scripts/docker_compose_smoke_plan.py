"""Print a Docker Compose smoke plan without executing Docker."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    compose = ROOT / "docker-compose.yml"
    if not compose.exists():
        raise SystemExit("docker-compose.yml is missing")
    print("Docker Compose smoke plan")
    print("1. cp .env.example .env")
    print("2. docker compose config")
    print("3. docker compose up --build")
    print("4. curl http://localhost:8080/health")
    print("5. open http://localhost:8081/index.html")
    print("Boundary: no live connectors, no live providers, no raw secrets")


if __name__ == "__main__":
    main()
