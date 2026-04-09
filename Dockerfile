FROM python:3.13-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv pip install --system ".[web]"

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY src/ src/
COPY notes/ notes/
COPY tutor_prompt.md .

ENV PYTHONPATH=/app/src
EXPOSE 8080
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
