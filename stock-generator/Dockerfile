FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install kafka-python faker
CMD ["python", "stock_generator.py"]
