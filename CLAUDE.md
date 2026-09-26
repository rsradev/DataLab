# DataLab

Personal learning/playground monorepo for data engineering, ML, and Python. Mostly course material (Jupyter notebooks) plus small standalone demo projects. There is no single app, build, or test suite — each subproject is independent.

## Layout

- `data/` — shared sample datasets (CSV/TXT) used by notebooks and Spark scripts. Ignored by git for new files; the existing ones are already tracked.
- `de-area/` — data engineering
  - `spark/` — PySpark notebooks (RDDs, DataFrames, SQL/UDFs, AQE, Delta, streaming) and `streaming.py`. Runs locally with `master('local[*]')`.
  - `kafka/kafka-app-demo/` — kafka-python producer/consumer demo (`requirements.txt`).
  - `templates/` — Kafka→Spark (Scala/sbt) and Spark→Cassandra job templates.
  - `dexpert/` — SQL practice.
- `ml-area/`
  - `edu/` — course notebooks: `ZTM/` (numpy, pandas, sklearn, PyTorch), `sundog-ml/` (stats, ML, Keras/TF, Spark MLlib, GenAI/OpenAI), `ml-coursera/`, `math-coursera/`, `hugging_face/` (uv project, Python ≥3.13).
  - `app/` — small applications (e.g. face recognition).
  - `kaggle/` — Kaggle work.
- `python-area/` — core Python topics: async, databases, decorators, OOP, design patterns, performance, debugging, testing (`pytestings/`), env tooling (`env-tut/` venv/pipenv/poetry demos), FastAPI projects (`restproject/` = poetry, `demo_server/` = requirements.txt).

## Environments

Each subproject manages its own dependencies — there is no root environment.
- `uv`: `ml-area/edu/hugging_face` → `uv sync`, `uv run ...`
- poetry: `python-area/restproject`, `python-area/env-tut/poetry_demo` → `poetry install`, `poetry run pytest`
- pip: folders with `requirements.txt` → create a venv in that folder, then `pip install -r requirements.txt`
- Python is managed with pyenv; Spark (`spark-submit`/pyspark) is installed via pyenv shims; Java is system.

## Running things

- Notebooks: `jupyter lab` from the repo root. To execute one headlessly: `jupyter nbconvert --to notebook --execute <file>.ipynb --output /tmp/out.ipynb`.
- Spark scripts: `spark-submit de-area/spark/streaming.py` (or `python` with pyspark installed).
- Tests: run pytest from the specific subproject, e.g. `cd python-area/pytestings/pytest && pytest`.
- Kafka/Cassandra demos need those services running locally (not included here).

## Conventions and gotchas

- Notebooks are the primary medium. When editing a notebook, edit cells (NotebookEdit) rather than rewriting the JSON, and don't commit large cell outputs.
- Relative data paths in notebooks usually point at `data/` or a sibling folder — check the notebook's working dir before changing paths.
- Do not touch `de-area/spark/metastore_db/` or `de-area/spark/spark-warehouse/` — they are Spark/Derby runtime artifacts.
- `.gitignore` ignores `*.csv`, `*.json`, `*.parquet` and `data/`. New datasets won't be committed unless force-added.
- Never commit secrets: API keys (OpenAI, Hugging Face, etc.) belong in `.env` (ignored).
- Commit messages so far are informal; keep commits scoped to one area when possible.
