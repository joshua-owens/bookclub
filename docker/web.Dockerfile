FROM python:3.11

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements*.txt /app/
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . /app/

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "bookclub.asgi:application"]
