FROM python:3.11-slim
WORKDIR /app
COPY . /app
EXPOSE 8080
CMD ["python", "server/node_server.py"]
