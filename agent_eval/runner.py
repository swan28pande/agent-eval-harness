import ray

from .scorers import SCORERS
from .trajectory import Trajectory


@ray.remote
def _evaluate(traj: Trajectory) -> dict:
    scores = {name: fn(traj) for name, fn in SCORERS.items()}
    return {"task_id": traj.task_id, "success": traj.success, **scores}


def evaluate_all(trajs: list[Trajectory]) -> list[dict]:
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True, include_dashboard=False)
    return ray.get([_evaluate.remote(t) for t in trajs])
