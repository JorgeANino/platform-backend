FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat gcc libpq-dev

COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt 

COPY . .

COPY entrypoint.sh .
COPY run_tests.sh .

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN sed -i 's/\r$//g' /app/run_tests.sh

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/run_tests.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
