# v1.6 Connector Contract SDK and Dry-Run Adapters

v1.6 introduces the connector contract layer. The goal is not live enterprise integration yet. The goal is to make connector behavior inspectable before runtime execution is allowed.

A connector contract declares:

- adapter identity
- connector identity
- allowed tenants and environments
- required service identities
- required secret references
- operation list
- operation side-effect class
- input and output schemas
- approval requirement
- rollback expectation
- dry-run behavior
- required controls

This means a connector can be reviewed before anyone writes live integration code.

## Design principle

The control plane should never treat a connector as a black box. Every operation must have a declared risk, side-effect class, environment scope, and rollback/compensation expectation.

## v1.6 boundary

v1.6 remains dry-run only:

- no ERP write-back
- no ticket creation
- no email send
- no HR system write
- no payment or invoice posting
- no real secret material
- no live connector authentication

## Why this matters

Enterprise agents become dangerous when tool execution is informal. The connector contract layer creates a reviewable interface between agent reasoning and system action.
