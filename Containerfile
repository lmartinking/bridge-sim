FROM python:3.12-slim-bookworm as build

# Install poetry
ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry==1.8.2

COPY . /app

WORKDIR /app
RUN python3 -m venv .venv
RUN $POETRY_HOME/bin/poetry install

FROM python:3.12-slim-bookworm

COPY --from=build /app /app

WORKDIR /app

CMD ["/app/.venv/bin/python", "-m", "bridgesim.main"]

EXPOSE 80

ENV PORT=80
ENV HOST=0.0.0.0
ENV ENV=PROD

LABEL org.opencontainers.image.source=https://github.com/lmartinking/bridge-sim
LABEL org.opencontainers.image.authors="Atticus Martin-King Tan"
