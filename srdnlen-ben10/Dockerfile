FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV=production
ENV FLAG="srdnlen{test_flag}"

CMD ["flask", "run", "--host=0.0.0.0"]
