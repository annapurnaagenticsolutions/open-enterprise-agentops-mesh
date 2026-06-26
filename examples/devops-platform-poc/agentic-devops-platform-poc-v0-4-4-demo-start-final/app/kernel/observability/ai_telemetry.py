from pydantic import BaseModel


class AITelemetry(BaseModel):
    workflow_id: str
    step: str
    model: str = "mock-claude-native"
    prompt_version: str = "poc.v0.2-lite"
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    estimated_cost_usd: float = 0.0
    latency_ms: int = 0
    context_items: int = 0
    retrieval_hit_rate: float = 0.0
    schema_valid: bool = True
    fallback_used: bool = False
    abstained: bool = False


def estimate_mock_telemetry(
    workflow_id: str,
    step: str,
    context_size_chars: int,
    output_size_chars: int,
    context_items: int,
    retrieval_hit_rate: float,
    abstained: bool = False,
) -> AITelemetry:
    input_tokens = max(1, context_size_chars // 4)
    output_tokens = max(1, output_size_chars // 4)
    estimated_cost = round(((input_tokens / 1_000_000) * 3.0) + ((output_tokens / 1_000_000) * 15.0), 6)
    return AITelemetry(
        workflow_id=workflow_id,
        step=step,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_tokens=int(input_tokens * 0.35),
        estimated_cost_usd=estimated_cost,
        latency_ms=120 + min(2500, input_tokens // 10),
        context_items=context_items,
        retrieval_hit_rate=retrieval_hit_rate,
        abstained=abstained,
    )
