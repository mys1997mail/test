FROM python:3-alpine
WORKDIR /app
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["src/hello.py"]
EXPOSE 5000
