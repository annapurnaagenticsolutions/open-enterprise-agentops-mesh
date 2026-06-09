from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Vendor-neutral LLM provider interface for future releases.

    v0.2 does not call live LLMs. This protocol defines the boundary for future
    OpenAI-compatible, Anthropic, Gemini, Ollama, vLLM, and mock providers.
    """

    provider_name: str

    def generate(self, prompt: str, *, system: str | None = None) -> str:
        raise NotImplementedError


class MockLLMProvider:
    provider_name = "mock"

    def generate(self, prompt: str, *, system: str | None = None) -> str:
        return "Mock provider response. Live LLM execution is planned for a later release."
