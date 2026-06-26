from __future__ import annotations

from pathlib import Path
import json

from agentops_mesh_api.models.schemas import ConnectorInfo, ConnectorRegistryResponse, ConnectorToolInfo, TargetEnvironment


class ConnectorRegistryService:
    """Static connector registry for sandbox-first enterprise tool access."""

    def __init__(self, registry_path: Path | None = None) -> None:
        if registry_path is None:
            root = Path(__file__).resolve().parents[4]
            registry_path = root / "connectors" / "sample_connectors.json"
        self.registry_path = registry_path

    def list_connectors(self) -> ConnectorRegistryResponse:
        payload = self._load()
        return ConnectorRegistryResponse(
            version=payload.get("version", "0.8.0"),
            connectors=[ConnectorInfo(**item) for item in payload.get("connectors", [])],
        )

    def get_connector(self, connector_id: str) -> ConnectorInfo:
        for connector in self.list_connectors().connectors:
            if connector.connector_id == connector_id:
                return connector
        raise KeyError(f"Connector not found: {connector_id}")

    def get_tool(self, connector_id: str, tool_id: str) -> tuple[ConnectorInfo, ConnectorToolInfo]:
        connector = self.get_connector(connector_id)
        for tool in connector.tools:
            if tool.tool_id == tool_id:
                return connector, tool
        raise KeyError(f"Tool not found: {connector_id}.{tool_id}")

    def is_allowed_in_environment(self, connector: ConnectorInfo, tool: ConnectorToolInfo, environment: TargetEnvironment) -> bool:
        env = environment.value
        return env in connector.allowed_environments and env in tool.allowed_environments

    def _load(self) -> dict:
        if not self.registry_path.exists():
            return {"version": "0.8.0", "connectors": []}
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

