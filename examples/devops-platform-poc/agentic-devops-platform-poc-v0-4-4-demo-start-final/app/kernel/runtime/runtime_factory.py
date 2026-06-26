from app.kernel.runtime.claude_agent_sdk_runtime import ClaudeAgentSdkRuntime
from app.kernel.runtime.claude_api_runtime import ClaudeApiRuntime
from app.kernel.runtime.langgraph_runtime import LangGraphRuntime
from app.kernel.runtime.mock_claude_runtime import MockClaudeRuntime
from app.kernel.runtime.runtime_modes import RuntimeMode


def build_agent_runtime(runtime_mode: RuntimeMode):
    if runtime_mode == RuntimeMode.MOCK_CLAUDE:
        return MockClaudeRuntime()
    if runtime_mode == RuntimeMode.CLAUDE_API:
        return ClaudeApiRuntime()
    if runtime_mode == RuntimeMode.CLAUDE_AGENT_SDK:
        return ClaudeAgentSdkRuntime()
    if runtime_mode == RuntimeMode.LANGGRAPH:
        return LangGraphRuntime()
    raise ValueError(f"Unsupported runtime mode: {runtime_mode}")
