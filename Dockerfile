FROM python:3.9

RUN apt-get update && apt-get install -y redis-server

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]