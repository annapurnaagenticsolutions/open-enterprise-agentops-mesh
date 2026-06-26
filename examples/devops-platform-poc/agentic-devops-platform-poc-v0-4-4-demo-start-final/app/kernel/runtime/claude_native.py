from typing import Any

from app.core.registry import PluginRegistry
from app.kernel.audit.in_memory_audit_logger import InMemoryAuditLogger
from app.kernel.context.context_builder import DefaultContextBuilder
from app.kernel.events.models import CanonicalEvent


class ClaudeNativeRuntime:
    def __init__(
        self,
        plugin_registry: PluginRegistry,
        context_builder: DefaultContextBuilder,
        audit_logger: InMemoryAuditLogger,
    ) -> None:
        self.plugin_registry = plugin_registry
        self.context_builder = context_builder
        self.audit_logger = audit_logger

    async def run(self, plugin_name: str, event: CanonicalEvent) -> dict[str, Any]:
        plugin = self.plugin_registry.get(plugin_name)
        context = await self.context_builder.build_context(event)
        await self.audit_logger.record(
            workflow_id=event.event_id,
            entry={
                "actor": "runtime",
                "action": "context_built",
                "details": {
                    "plugin_name": plugin_name,
                    "log_count": len(context.logs),
                    "memory_matches": len(context.memory_matches),
                    "schema_version": event.schema_version,
                    "idempotency_key": event.idempotency_key,
                },
            },
        )
        return await plugin.execute(context)
