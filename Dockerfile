FROM python:3-alpine
WORKDIR /app
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src /app
ENTRYPOINT ["python"]
CMD ["hello.py"]
EXPOSE 5000
