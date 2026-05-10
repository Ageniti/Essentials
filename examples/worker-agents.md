# Worker Agents

Essentials supports background worker agents through the subprocess-based swarm
path.

Typical pattern:

1. Start the main runtime.
2. Spawn a worker agent for a focused task.
3. Read worker output.
4. Send follow-up instructions if needed.

Related tools:

- `agent(...)`
- `send_message(to=..., message=...)`
- `task_output(task_id=...)`

This is intended for practical local parallelism, not a large multi-backend
orchestration platform.
