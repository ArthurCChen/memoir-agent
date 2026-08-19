# MEMOIR

This repository starts from the `verl-agent` data model and adds an audit-first
pipeline for studying information lifecycle failures in grouped agent rollouts.

The first milestone is intentionally observational. It exports same-prompt
trajectory groups, preserves the exact policy-visible context and raw evidence,
and creates grounded human-annotation queues. It does not infer causal effects.

## Layout

- `experiments/trajectory_audit/`: export, queue building, schemas, and tests.
- `docs/research/trajectory-audit-findings.md`: source audit and design notes.
- `docs/reproducibility/trajectory-audit.md`: teammate-facing reproduction guide.

## Quick check

```bash
python -m unittest discover -s experiments/trajectory_audit/tests -v
```

## GPU workers

Clone `https://github.com/ArthurCChen/memoir-agent.git`, open Claude Code in the
repository root, and tell it whether the host is `machine-a` or `machine-b`.
Claude Code starts from `CLAUDE.md` and follows the corresponding file in
`worker_tasks/`.

The official-method reproduction matrix and confirmed stock logging boundary
are documented in `docs/reproducibility/original-methods.md`.

## Upstream base

The intended base is `langfengQ/verl-agent` at revision
`20bd331bdbc9026a5668e11362178e10ab7400c8`. The audit tools are kept separate
until a raw rollout batch is available, so this repository can be tested on a
CPU-only machine and applied to an exact upstream checkout on a GPU machine.
