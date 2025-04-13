FROM python:3.12

WORKDIR /app

# Python Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App
COPY . .

EXPOSE 8080
CMD ["python", "identifier_server.py"]