from app.kernel.context.models import WorkflowContext
from app.kernel.events.models import CanonicalEvent


class DefaultContextBuilder:
    def __init__(self, cicd_adapter, scm_adapter, ticket_adapter, memory_store):
        self.cicd_adapter = cicd_adapter
        self.scm_adapter = scm_adapter
        self.ticket_adapter = ticket_adapter
        self.memory_store = memory_store

    async def build_context(self, event: CanonicalEvent) -> WorkflowContext:
        logs = await self.cicd_adapter.get_build_logs(event.build_id or "")
        build_metadata = await self.cicd_adapter.get_build_metadata(event.build_id or "")
        pipeline_config = await self.cicd_adapter.get_pipeline_config(event.pipeline_id or "")

        commit_diff = {}
        manifests = []

        if event.metadata.get("scenario") != "weak_evidence" and event.repository and event.commit_sha:
            commit_diff = await self.scm_adapter.get_commit_diff(
                repo=event.repository,
                commit_sha=event.commit_sha,
            )
            manifests = await self.scm_adapter.get_dependency_manifests(
                repo=event.repository,
                ref=event.commit_sha,
            )

        context = WorkflowContext(
            event=event,
            logs=logs,
            build_metadata=build_metadata,
            pipeline_config=pipeline_config,
            commit_diff=commit_diff,
            manifests=manifests,
            history=[],
            memory_matches=[],
        )
        context.memory_matches = await self.memory_store.search_patterns(context)
        return context
