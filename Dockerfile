FROM python:3.11-slim

WORKDIR /usr/src/app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

RUN mkdir -p /usr/src/app/static

COPY . .

RUN chmod -R 755 /usr/src/app/static

EXPOSE 7654

CMD ["python", "manage.py", "runserver", "0.0.0.0:7654"]