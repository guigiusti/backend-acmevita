FROM python:3.13.5

RUN addgroup --system app && adduser --system --ingroup app --home /code --shell /sbin/nologin app

WORKDIR /code

COPY --chown=app:app requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=app:app ./app /code/app

USER app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--forwarded-allow-ips", "*", "--access-logfile", "-", "--log-level", "info"]