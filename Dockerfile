FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Never re-resolve the lockfile at runtime, and copy rather than hardlink so the
# venv survives being built on one filesystem and bind-mounted over on another.
ENV UV_FROZEN=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first: this layer is cached until pyproject/uv.lock actually change.
# Dev tools are included -- this is the image used to run the tests and linter too.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
