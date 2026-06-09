# Secret Boundary and No-Raw-Secret Policy

v1.5 establishes a strict rule:

> The repository may contain secret references and metadata, but never secret material.

## Allowed

- secret reference IDs,
- sensitivity classification,
- owner team,
- allowed identity IDs,
- allowed connector IDs,
- rotation policy text,
- required control names.

## Not allowed

- API keys,
- OAuth client secrets,
- refresh tokens,
- private keys,
- database passwords,
- cloud credentials,
- live connector credentials.

## Future external vault integration

Later versions may integrate with:

- HashiCorp Vault,
- AWS Secrets Manager,
- Azure Key Vault,
- Google Secret Manager,
- Kubernetes Secrets with sealed/encrypted controls.

But v1.5 deliberately keeps this at reference-contract level only.
