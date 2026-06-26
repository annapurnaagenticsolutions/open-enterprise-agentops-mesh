# v2.4 Public FAQ and Objection Handling

## Is this another agent framework?

No. It is a control-plane framework around enterprise agents. It does not try to replace LangGraph, CrewAI, AutoGen, Semantic Kernel, or custom orchestrators. It governs whether agents, tools, models, and actions should be allowed.

## Does it call live model providers?

No. Live model-provider execution remains intentionally disabled. The project models provider governance, routing decisions, risk controls, and safety review first.

## Does it connect to real enterprise systems?

No. Connector execution is sandbox-first and dry-run based. Live connector readiness is evaluated, but live execution remains disabled.

## Why deterministic rules instead of LLM-based governance?

Enterprise enforcement should be explainable and auditable. LLMs can assist with recommendations, but core gates should be deterministic first.

## Who is this for?

Enterprise architects, AI product managers, platform engineering teams, governance leaders, and developers building serious agent programs.

## What makes this useful commercially?

It can support assessment workshops, architecture reviews, governance scorecards, implementation planning, and vertical accelerators such as procurement or IT support.

## What is the current maturity?

v2.4 is a strong public MVP and reference implementation. It is not production-ready for regulated deployment without additional IAM, database, vault, observability, and security hardening.
