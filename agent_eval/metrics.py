from prometheus_client import Counter, Histogram, start_http_server

TRAJECTORIES = Counter("agent_eval_trajectories_total", "Trajectories evaluated")
SCORE = Histogram(
    "agent_eval_score",
    "Per-trajectory score by dimension",
    ["scorer"],
    buckets=[i / 10 for i in range(11)],
)


def serve(port: int = 8000) -> None:
    start_http_server(port)


def record(scores: dict[str, float]) -> None:
    TRAJECTORIES.inc()
    for name, value in scores.items():
        SCORE.labels(scorer=name).observe(value)
