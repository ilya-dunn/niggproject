FROM python:3.12-alpine
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn sitenigger.wsgi:application --bind 0.0.0.0:8000"]