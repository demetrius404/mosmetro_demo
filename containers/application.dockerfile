FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["gunicorn"]
CMD ["--workers", "5", "--bind", "0.0.0.0:8000", "application:app"]