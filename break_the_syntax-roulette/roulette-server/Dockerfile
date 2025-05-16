FROM python:3.11-slim

# Install socat
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Copy files
COPY server_roulette.py /app/roulette.py
COPY flag /app/flag
WORKDIR /app

# Entry point: forward TCP 1337 to stdin/stdout of the Python script
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 roulette.py",pty,stderr
