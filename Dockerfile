FROM python:alpine
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY pluseen pluseen
CMD ["gunicorn", "--bind", "0.0.0.0:80", "pluseen:create_app()"]
