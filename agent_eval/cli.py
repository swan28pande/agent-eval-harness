import argparse
import json
import time

from . import metrics
from .runner import evaluate_all
from .scorers import SCORERS
from .trajectory import load_jsonl


def main() -> None:
    p = argparse.ArgumentParser(description="Score agent trajectories.")
    p.add_argument("path", help="JSONL file of trajectories")
    p.add_argument("--metrics-port", type=int, default=0, help="Serve Prometheus metrics on this port")
    p.add_argument("--hold", action="store_true", help="Keep serving metrics after evaluation")
    args = p.parse_args()

    if args.metrics_port:
        metrics.serve(args.metrics_port)

    results = evaluate_all(load_jsonl(args.path))
    for r in results:
        metrics.record({k: r[k] for k in SCORERS})
        print(json.dumps(r))

    n = len(results)
    summary = {k: round(sum(r[k] for r in results) / n, 3) for k in SCORERS} if n else {}
    print(json.dumps({"summary": summary, "n": n}))

    while args.hold:
        time.sleep(60)


if __name__ == "__main__":
    main()
