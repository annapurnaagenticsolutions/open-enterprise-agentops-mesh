# Monitoring Noise & Alert Fatigue

Problem
- Excessive alerts with low signal quality; operators overwhelmed; danger of missing critical events.

Agentic Solution (Pattern)
- Monitoring & Observability Agent: alert correlation, RCA hypotheses, runbooks or auto-remediation where safe; create actionable tasks or suppress non-critical alerts.
- Data & Integrations: Datadog/Prometheus/Splunk/NR, ticketing, runbooks.
- HITL gates for high-severity alerts; tuning feedback loop to improve thresholds.

Success Metrics
- Alert volume reduction, MTTD, automation conversion rate, operator satisfaction.

Risks and Mitigations
- Over-suppression; ensure HITL for critical alerts; maintain visibility.

Example Prompts/Templates
- RCA prompts, suppression policy prompts.
