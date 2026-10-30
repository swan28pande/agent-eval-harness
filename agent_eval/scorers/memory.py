from ..trajectory import Trajectory


def score_memory(traj: Trajectory) -> float:
    """Fraction of memory writes that are read back in a later step."""
    writes = {i: s.memory_write for i, s in enumerate(traj.steps) if s.memory_write}
    if not writes:
        return 1.0
    used = 0
    for i, key in writes.items():
        if any(s.memory_read == key for s in traj.steps[i + 1 :]):
            used += 1
    return used / len(writes)
