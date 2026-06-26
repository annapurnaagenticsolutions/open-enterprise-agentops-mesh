# Simulator Isolation Audit — v0.5.1

## Problem reported

The Business simulator scenario selection did not update Key services. Earlier builds also made some simulator outputs feel mixed because shared output phrasing and long-page structure blurred simulator boundaries.

## Correction approach

### 1. Data separation

Scenario-specific data is now stored under separate objects:

- `businessScenarios`
- `educationTopics`
- `safetyScenarios`

### 2. Field prefix isolation

Each simulator uses unique field prefixes:

- Business: `business*`
- Education: `edu*`
- Digital Safety: `safety*`
- Multi-Agent Workflow: `workflow*`
- Opportunity Evaluator: `opportunity*`

### 3. Generator isolation

Each simulator has a separate generator function:

- `generateBusiness`
- `generateEducation`
- `generateSafety`
- `generateWorkflow`
- `generateOpportunity`

### 4. Dynamic dependency fix

`simulators-page.js` listens to form changes. When `businessScenario` changes, it applies the selected scenario's defaults to:

- `businessName`
- `businessLocation`
- `businessServices`

This directly fixes the issue where Key services remained stale.

## Validation result

Manual code inspection and automated smoke checks confirm that the Business scenario data is not static anymore and services update per selected scenario.
