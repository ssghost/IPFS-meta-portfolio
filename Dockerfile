FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install pdm
RUN pdm install

RUN mkdir -p /app/chroma_db && chmod -R 777 /app

ENV PORT=7860

CMD ["pdm", "run", "python", "-m", "app.engine.router"]