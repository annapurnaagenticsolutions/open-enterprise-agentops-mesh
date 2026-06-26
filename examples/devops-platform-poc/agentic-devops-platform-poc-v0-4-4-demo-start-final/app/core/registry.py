from dataclasses import dataclass, field
from typing import Any


@dataclass
class AdapterRegistry:
    cicd_adapters: dict[str, Any] = field(default_factory=dict)
    scm_adapters: dict[str, Any] = field(default_factory=dict)
    ticket_adapters: dict[str, Any] = field(default_factory=dict)

    def register_cicd(self, name: str, adapter: Any) -> None:
        self.cicd_adapters[name] = adapter

    def register_scm(self, name: str, adapter: Any) -> None:
        self.scm_adapters[name] = adapter

    def register_ticketing(self, name: str, adapter: Any) -> None:
        self.ticket_adapters[name] = adapter

    def get_cicd(self, name: str) -> Any:
        return self.cicd_adapters[name]

    def get_scm(self, name: str) -> Any:
        return self.scm_adapters[name]

    def get_ticketing(self, name: str) -> Any:
        return self.ticket_adapters[name]


@dataclass
class PluginRegistry:
    plugins: dict[str, Any] = field(default_factory=dict)

    def register(self, plugin: Any) -> None:
        self.plugins[plugin.name] = plugin

    def get(self, name: str) -> Any:
        return self.plugins[name]
