FROM python:3.13-slim-bookworm

WORKDIR /app
RUN python3 -m pip install --no-cache-dir flask gunicorn
COPY app.py flag.txt /app/

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:3000", "app:app"]
