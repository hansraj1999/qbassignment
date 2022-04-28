FROM python:3.10
WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY . /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
