# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in AgentOps Mesh, please report it responsibly:

1. Email: hello@annapurna.ai
2. Subject: `[SECURITY] AgentOps Mesh - <brief description>`
3. Include: description of the vulnerability, reproduction steps, potential impact

**Do not open a public GitHub issue for security vulnerabilities.**

## Response timeline

- Acknowledgment: within 48 hours
- Initial assessment: within 7 days
- Fix or mitigation: depends on severity, communicated via email

## Scope

- Policy enforcement bypass
- Audit trail manipulation
- Sandbox escape
- Connector credential exposure
- API authentication/authorization issues

## Out of scope

- Issues in user-defined policies (users are responsible for their own policy content)
- Issues in third-party LLM providers accessed through connectors
- Issues in deployed infrastructure (users are responsible for their own deployment security)
