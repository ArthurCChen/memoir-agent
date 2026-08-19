# Download-Only GPU Worker Runbook

## 1. Select the lane

- Machine A reads `worker_tasks/machine-a.md`.
- Machine B reads `worker_tasks/machine-b.md`.

Machine A covers GraphGPO and GiGPO; Machine B covers HGPO and an independent
audit-readiness check. Both lanes implement the same logging contract. This is deliberate:
the machines cannot exchange patches, so neither lane may depend on unpublished
changes from the other.

## 2. Prepare the checkout

Clone this repository and the pinned upstream revision in sibling directories:

```bash
mkdir -p memoir-work && cd memoir-work
git clone https://github.com/ArthurCChen/memoir-agent.git memoir
git clone https://github.com/langfengQ/verl-agent.git verl-agent
cd verl-agent
git checkout 20bd331bdbc9026a5668e11362178e10ab7400c8
git submodule update --init --recursive
```

Do not proceed on a different upstream revision. Record a blocker if the commit
cannot be fetched.

## 3. Capture a sanitized manifest

Create `memoir/reports/<machine-id>/manifest.txt` containing versions and GPU
information. Remove usernames, hostnames, IP addresses, tokens, storage mount
paths, and scheduler account names before rendering any screenshot.

Required entries are upstream revision, MEMOIR revision, Python version,
PyTorch version, CUDA runtime, NVIDIA driver, GPU type/count, environment/data
revision, model revision, and exact non-secret launch overrides.

## 4. Implement the audit logging contract

Locate the actual GraphGPO/GiGPO rollout collector symbols in the pinned source;
do not rely on line numbers in this document. Add a configuration-gated audit
path that leaves default training behavior unchanged.

Every step record must contain:

- `uid` and `traj_uid`;
- explicit `step_index` and task-instance identifier;
- exact structured chat/messages before tokenization;
- `model_context_text` and, when available, `rendered_prompt_text`;
- `anchor_obs` and `next_obs` as separate raw fields;
- decoded model action and post-parser `executed_action`;
- step reward, terminal status, and verifier output;
- memory snapshot with immutable provenance identifiers, or an explicit
  `memory_not_available` marker;
- environment seed and a replay-capability description.

Store large step payloads in append-only JSONL. The serialized DataProto may
contain stable references to those records rather than duplicating them. Flush
atomically at trajectory boundaries. A partial or failed trajectory must remain
inspectable.

## 5. Add tests before GPU collection

At minimum, test:

- eight trajectories from one prompt share `uid` and have unique `traj_uid`;
- step indices are contiguous within a trajectory even when rows are interleaved;
- raw observation and model-visible context are not aliased;
- decoded and executed actions can differ and both survive export;
- non-ASCII character and byte offsets remain stable;
- interrupted writes leave earlier complete trajectories readable;
- audit logging disabled preserves existing behavior.

Run upstream relevant tests plus:

```bash
cd ../memoir
python -m unittest discover -s experiments/trajectory_audit/tests -v
```

## 6. Run the pilot

Use ALFWorld, `env.rollout.n=8`, deterministic recorded seeds, and a small
rollout-only/evaluation job. Start with one prompt group. Validate it before
expanding to at least five prompt groups. Never start full RL training in this
stage.

Before adding a logger, search the stock code and configuration for existing
trajectory/batch persistence. For each method, record:

- enabling config and exact launch override;
- writer function and on-disk format;
- whether all same-prompt rollouts or only aggregate metrics are saved;
- whether exact prompts, observations, model actions, executed actions, rewards,
  termination, and trajectory identity survive serialization;
- whether a provided reader/visualizer can reconstruct the full trajectory.

Reuse stock persistence when it satisfies the contract. Extend it minimally
when it does not. Never maintain two competing trajectory formats without a
documented stable mapping.

Export and validate:

```bash
cd ../memoir
python -m experiments.trajectory_audit.export_rollouts \
  /path/to/local/batch.pth reports/<machine-id>/audit \
  --source-revision 20bd331bdbc9026a5668e11362178e10ab7400c8

python -m experiments.trajectory_audit.validate_export \
  reports/<machine-id>/audit/rollouts.jsonl

python -m experiments.trajectory_audit.build_annotation_queue \
  reports/<machine-id>/audit/rollouts.jsonl \
  reports/<machine-id>/audit/annotation_queue.jsonl
```

If there is no success/failure contrast, record that fact. Do not relabel
outcomes to manufacture contrast.

## 7. Produce the photograph target

Fill `reports/<machine-id>/result.json` according to
`worker_tasks/result.schema.json`. Then run:

```bash
python scripts/render_handoff.py \
  reports/<machine-id>/result.json \
  reports/<machine-id>/handoff-summary.svg
```

Open the SVG full screen at 100% zoom. Confirm all text fits, the modified-file
list is complete, and no private information appears. The operator photographs
this single screen.
