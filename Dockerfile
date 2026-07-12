FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]