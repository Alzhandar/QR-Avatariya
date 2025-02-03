FROM python:3.11-slim

WORKDIR /usr/src/app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 7654

CMD ["python", "manage.py", "runserver", "0.0.0.0:7654"]