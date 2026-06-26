import asyncio
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.kernel.cache.prompt_cache_policy import PromptCachePolicy
from app.kernel.runtime.agent_runtime_contract import ContextPack
from app.kernel.runtime.runtime_factory import build_agent_runtime
from app.kernel.runtime.runtime_modes import RuntimeMode, WorkflowStep
from app.kernel.tools.tool_schema_registry import build_default_tool_definitions


async def main() -> None:
    modes = [
        RuntimeMode.MOCK_CLAUDE,
        RuntimeMode.CLAUDE_API,
        RuntimeMode.CLAUDE_AGENT_SDK,
        RuntimeMode.LANGGRAPH,
    ]
    results = []
    for mode in modes:
        runtime = build_agent_runtime(mode)
        result = await runtime.run_step(
            step_name=WorkflowStep.GENERATE_RCA,
            context_pack=ContextPack(
                workflow_id=f"runtime-demo-{mode.value}",
                step_name=WorkflowStep.GENERATE_RCA,
                event_summary={"scenario": "dependency_conflict_with_docs_gap"},
            ),
            allowed_tools=build_default_tool_definitions()[:4],
            output_schema={"type": "object"},
            cache_policy=PromptCachePolicy(),
        )
        results.append(result.model_dump())
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
