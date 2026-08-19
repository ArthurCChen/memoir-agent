# Instructions for Claude Code

You are operating a download-only strong-GPU worker for the MEMOIR project.
Read `AGENTS.md` and `WORKER_INSTRUCTIONS.md` completely before changing code.

If `worker_tasks/` is absent after cloning but `worker_bundle.tar.gz` is present,
run `python bootstrap_worker.py` once, then continue reading. Do not delete the
bundle; it is the immutable source artifact for the download-only handoff.

The human will not copy source files or logs back to the coordinating machine.
Your final communication channel is one photograph of
`reports/<machine-id>/handoff-summary.svg`. Therefore:

1. make the result JSON concise but complete;
2. use exact repository-relative paths and short commit SHAs;
3. include failed tests and blockers, not only successes;
4. ensure the SVG contains no secrets, hostnames, usernames, or absolute paths;
5. do not report a trajectory audit as complete if exact policy context is
   missing.

Start by asking the operator whether this machine is `machine-a` or `machine-b`.
Machine A reproduces GraphGPO and GiGPO; Machine B reproduces HGPO. Then follow
only the corresponding task file. You may modify the local checkout
and install dependencies. You must not upload or push anything.
