from __future__ import annotations

from pathlib import Path
import json

from agentops_mesh_api.models.schemas import ProviderInfo, ProviderRegistryResponse, TargetEnvironment


class ProviderRegistryService:
    """Loads provider/model registry from local JSON.

    v0.6 keeps this static and inspectable. Future releases can move provider
    metadata into the Agent Registry or a database-backed configuration store.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        if registry_path is None:
            root = Path(__file__).resolve().parents[4]
            registry_path = root / "runtime" / "provider_registry.json"
        self.registry_path = registry_path

    def list_providers(self) -> ProviderRegistryResponse:
        payload = self._load()
        return ProviderRegistryResponse(
            version=payload.get("version", "0.6.0"),
            providers=[ProviderInfo(**item) for item in payload.get("providers", [])],
        )

    def select_provider(
        self,
        target_environment: TargetEnvironment,
        preferred_provider: str | None = None,
        preferred_model: str | None = None,
    ) -> tuple[ProviderInfo, str, str]:
        registry = self.list_providers()
        provider = self._find_provider(registry.providers, preferred_provider, target_environment)
        model_id = preferred_model or (provider.models[0].model_id if provider.models else "")
        model_ids = {model.model_id for model in provider.models}
        if model_id not in model_ids and provider.models:
            model_id = provider.models[0].model_id
        rationale = (
            f"Selected provider '{provider.provider_id}' for {target_environment.value}. "
            f"Model '{model_id}' selected by preference or provider default."
        )
        return provider, model_id, rationale

    def _find_provider(
        self,
        providers: list[ProviderInfo],
        preferred_provider: str | None,
        target_environment: TargetEnvironment,
    ) -> ProviderInfo:
        candidates = [p for p in providers if target_environment.value in p.allowed_environments]
        if preferred_provider:
            for provider in candidates:
                if provider.provider_id == preferred_provider:
                    return provider
        for provider in candidates:
            if provider.provider_id == "mock-safe-local":
                return provider
        if candidates:
            return candidates[0]
        raise ValueError(f"No provider is allowed for environment '{target_environment.value}'.")

    def _load(self) -> dict:
        if not self.registry_path.exists():
            return {"version": "0.6.0", "providers": []}
        return json.loads(self.registry_path.read_text(encoding="utf-8"))
