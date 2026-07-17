# use the dev hardened image that contains pip, a shell and build tools
FROM dhi.io/python:3.14-dev AS build-stage

# copy uv binaries from the uv image into this stage's image
COPY --from=dhi.io/uv:3.14-dev /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# use production hardened image for runtime (minimal)
FROM dhi.io/python:3.14 AS runtime-stage

WORKDIR /app
COPY --from=build-stage /app/.venv .venv
COPY src ./src
COPY alembic.ini .
COPY docker-entrypoint.sh .
RUN chmod 777 docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

EXPOSE 8000

CMD [".venv/bin/fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]