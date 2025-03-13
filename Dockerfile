FROM python:3.12

WORKDIR /app

# Python Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App
COPY LeafQuest .

# Ensure DEBUG = False
RUN sed -i 's/DEBUG = True/DEBUG = False/' LeafQuest/settings.py

# Rebuild Database
RUN python manage.py flush --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
