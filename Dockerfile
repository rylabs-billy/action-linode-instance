# Dockerfile
FROM python:alpine3.20

COPY requirements.txt .
RUN pip install --upgrade pip && \
  pip3 install --no-cache-dir -r requirements.txt

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python", "/entrypoint.py"]