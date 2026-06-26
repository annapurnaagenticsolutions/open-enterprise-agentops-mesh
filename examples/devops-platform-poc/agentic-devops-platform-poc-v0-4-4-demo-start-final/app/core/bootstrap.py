from app.adapters.cicd.mock_jenkins import MockJenkinsAdapter
from app.adapters.cicd.mock_teamcity import MockTeamCityAdapter
from app.adapters.scm.mock_gitlab import MockGitLabAdapter
from app.adapters.ticketing.mock_jira import MockJiraAdapter
from app.core.registry import AdapterRegistry, PluginRegistry
from app.kernel.audit.in_memory_audit_logger import InMemoryAuditLogger
from app.kernel.context.context_builder import DefaultContextBuilder
from app.kernel.memory.in_memory_pattern_store import InMemoryPatternStore
from app.kernel.policy.policy_engine import DefaultPolicyEngine
from app.kernel.runtime.claude_native import ClaudeNativeRuntime
from app.plugins.self_healing_pipeline.plugin import SelfHealingPipelinePlugin


def build_default_runtime(cicd_provider: str = "teamcity") -> ClaudeNativeRuntime:
    adapters = AdapterRegistry()
    adapters.register_cicd("teamcity", MockTeamCityAdapter())
    adapters.register_cicd("jenkins", MockJenkinsAdapter())
    adapters.register_scm("gitlab", MockGitLabAdapter())
    adapters.register_ticketing("jira", MockJiraAdapter())

    memory_store = InMemoryPatternStore.with_default_patterns()
    audit_logger = InMemoryAuditLogger()
    policy_engine = DefaultPolicyEngine()

    context_builder = DefaultContextBuilder(
        cicd_adapter=adapters.get_cicd(cicd_provider),
        scm_adapter=adapters.get_scm("gitlab"),
        ticket_adapter=adapters.get_ticketing("jira"),
        memory_store=memory_store,
    )

    plugin = SelfHealingPipelinePlugin(
        policy_engine=policy_engine,
        audit_logger=audit_logger,
        memory_store=memory_store,
    )

    plugins = PluginRegistry()
    plugins.register(plugin)

    return ClaudeNativeRuntime(
        plugin_registry=plugins,
        context_builder=context_builder,
        audit_logger=audit_logger,
    )
