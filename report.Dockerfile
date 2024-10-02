FROM python:3.10-alpine

RUN pip install mysql-connector-python==9.0.0

WORKDIR /app


ENV HOST="" \
    DB_USER_NAME="" \
    DB_USER_PASSWORD="" \
    DB_NAME=""

COPY ./report_generate.py /app
    
CMD ["python", "report_generate.py"]