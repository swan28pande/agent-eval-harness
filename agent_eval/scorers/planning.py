import torch

from ..trajectory import Trajectory


def _embed(texts: list[str], dim: int = 256) -> torch.Tensor:
    """Bag-of-words hashing embedding. Swap in a learned encoder here."""
    out = torch.zeros(len(texts), dim)
    for i, t in enumerate(texts):
        for tok in t.lower().split():
            out[i, hash(tok) % dim] += 1.0
    return torch.nn.functional.normalize(out, dim=-1)


def score_planning(traj: Trajectory) -> float:
    """Plan coverage (each plan item matched by some step) minus a redundancy penalty."""
    if not traj.plan or not traj.steps:
        return 0.0
    step_text = [f"{s.thought} {s.tool or ''}" for s in traj.steps]
    sim = _embed(traj.plan) @ _embed(step_text).T
    coverage = (sim.max(dim=1).values > 0.3).float().mean().item()
    calls = [(s.tool, str(sorted(s.args.items()))) for s in traj.steps if s.tool]
    redundancy = 1 - len(set(calls)) / len(calls) if calls else 0.0
    return max(0.0, coverage - 0.5 * redundancy)
