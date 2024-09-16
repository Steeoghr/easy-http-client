# Usa un'immagine Python ufficiale come base
FROM python:3.9-slim as python-base

# Poetry configuration
ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VENV="/opt/poetry-venv"
ENV POETRY_CACHE_DIR="/opt/.cache"

# Imposta la directory di lavoro nel container
WORKDIR /app

# Installa poetry separatamente
# Questa configurazione permette di avere layer Docker più piccoli e più facili da aggiornare
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Aggiungi `poetry` a PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copia solo i file necessari per installare le dipendenze
COPY pyproject.toml poetry.lock* ./

# Installa le dipendenze
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copia il resto del codice sorgente
COPY . .

# Imposta le variabili d'ambiente necessarie
ENV PYTHONUNBUFFERED=1

# Esegui lo script quando il container viene avviato
CMD ["python", "main.py"]