# Agent Eval Harness

An evaluation framework for multi-step agentic tasks. It scores **planning quality**, **memory utilization**, and **tool-use accuracy** through automated trajectory analysis.

Stack: Python, PyTorch, Ray, Docker, Prometheus.

## How it works

1. An agent run is recorded as a **trajectory**: a list of steps (thought, tool call, observation, memory reads/writes).
2. Each **scorer** analyzes the trajectory and returns a score in `[0, 1]`.
3. The **runner** evaluates many trajectories in parallel with Ray and exports metrics to Prometheus.

| Scorer | What it measures |
|---|---|
| `planning` | Plan coverage vs. executed steps, redundant steps |
| `memory` | Share of written memories that are later read and used |
| `tool_use` | Valid tool names, well-formed args, tool error rate |

## Quickstart

```bash
pip install -e .
python -m agent_eval.cli examples/trajectories.jsonl
```

With Docker (includes Prometheus):

```bash
docker compose up --build
```

Metrics are served on `:8000/metrics`, and Prometheus runs on `:9090`.

## Layout

```
agent_eval/
  trajectory.py   # Trajectory / Step data model
  scorers/        # planning, memory, tool_use
  runner.py       # Ray-parallel evaluation
  metrics.py      # Prometheus exporters
  cli.py          # entry point
```

## Status

Early skeleton. Scorers are heuristic for now; the PyTorch embedding hook in `scorers/planning.py` is the place to plug in learned similarity models.
