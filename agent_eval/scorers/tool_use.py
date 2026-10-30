from ..trajectory import Trajectory


def score_tool_use(traj: Trajectory) -> float:
    """Share of tool calls that use a known tool, pass dict args, and don't error."""
    calls = [s for s in traj.steps if s.tool]
    if not calls:
        return 0.0
    ok = sum(
        1
        for s in calls
        if s.tool in traj.available_tools and isinstance(s.args, dict) and not s.error
    )
    return ok / len(calls)
