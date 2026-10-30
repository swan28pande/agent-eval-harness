FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY agent_eval ./agent_eval
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -e .
COPY examples ./examples
EXPOSE 8000
CMD ["python", "-m", "agent_eval.cli", "examples/trajectories.jsonl", "--metrics-port", "8000", "--hold"]
