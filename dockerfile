FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

CMD daphne -b 0.0.0.0 -p  $PORT --application-close-timeout 60 wnp_exe.asgi:application
#CMD python manage.py runserver 0.0.0.0:8000