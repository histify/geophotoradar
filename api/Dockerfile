FROM python:3.12.5-alpine3.20 AS poetry
WORKDIR /app
RUN --mount=type=cache,id=poetry-pip,target=/root/.cache \
    python -m pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
RUN --mount=type=cache,id=poetry,target=/root/.cache \
    poetry lock && \
    poetry export -o requirements.txt && \
    poetry export -o requirements-test.txt --only test && \
    poetry export -o requirements-lint.txt --only lint


FROM python:3.12.5-alpine3.20 AS builder
WORKDIR /app
RUN adduser -D -h /app app
COPY --from=poetry /app/requirements.txt /app/
RUN --mount=type=cache,id=builder-pip,target=/root/.cache \
    python -m pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt


FROM builder AS dev
USER app

FROM builder AS test
COPY --from=poetry /app/requirements.txt /app/requirements-test.txt /app/requirements-lint.txt /app/
RUN --mount=type=cache,id=test,target=/root/.cache \
    pip install --no-cache-dir \
    -r requirements.txt \
    -r requirements-test.txt \
    -r requirements-lint.txt
COPY pyproject.toml .flake8 /app/
COPY app/ /app/app/
COPY tests/ /app/tests/
USER app


FROM builder AS prod
COPY app/ /app/app/
USER app
