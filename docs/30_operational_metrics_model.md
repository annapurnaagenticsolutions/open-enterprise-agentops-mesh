# Operational Metrics Model

## Metric groups

v0.7 introduces four metric groups.

### 1. Execution metrics

These describe runtime behavior.

- total traces
- executed count
- executed with controls count
- blocked count
- blocked pending approval count
- allowed run ratio
- blocked run ratio

### 2. Policy metrics

These describe governance friction.

- policy decision counts
- most common required controls
- most common required evidence
- high-severity block patterns
- external-action control frequency

### 3. Cost and usage metrics

These describe operational consumption.

- token estimate
- estimated cost
- cost by provider
- cost by agent
- average tokens per run

### 4. Agent-level metrics

These describe agent health and operating behavior.

- total runs by agent
- latest runtime decision
- blocked runs by agent
- allowed runs by agent
- total estimated cost by agent
- recent trace history

## Why estimates instead of billing truth

v0.7 uses deterministic cost estimates because providers differ in billing models and the current runtime uses mock providers. Future live-provider adapters should capture actual token usage and provider billing details when available.

## Recommended dashboard narrative

The observability console should answer four executive questions:

1. Are agents operating safely?
2. Which agents are blocked and why?
3. What is the cost and usage trend?
4. Which governance controls are creating recurring friction?
