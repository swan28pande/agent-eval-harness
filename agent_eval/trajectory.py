import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Step:
    thought: str = ""
    tool: str | None = None
    args: dict = field(default_factory=dict)
    observation: str = ""
    error: bool = False
    memory_write: str | None = None
    memory_read: str | None = None


@dataclass
class Trajectory:
    task_id: str
    plan: list[str]
    steps: list[Step]
    available_tools: list[str]
    success: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "Trajectory":
        return cls(
            task_id=d["task_id"],
            plan=d.get("plan", []),
            steps=[Step(**s) for s in d.get("steps", [])],
            available_tools=d.get("available_tools", []),
            success=d.get("success", False),
        )


def load_jsonl(path: str | Path) -> list[Trajectory]:
    with open(path) as f:
        return [Trajectory.from_dict(json.loads(line)) for line in f if line.strip()]
