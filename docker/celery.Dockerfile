FROM python:3.11

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["/usr/local/bin/celery", "-A", "myproject", "worker", "--loglevel=info"]