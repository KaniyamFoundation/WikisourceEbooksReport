FROM python:3.10-alpine

RUN pip3 install requests

WORKDIR /app


ENV GZIP_FILE="" \
    OUTDIR="" \
    SQL_FILENAME="" \
    GZIP_FILENAME=""

COPY ./download_db.py /app
CMD ["python", "download_db.py"]
