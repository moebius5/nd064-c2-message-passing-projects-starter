FROM python:3.8-alpine
LABEL maintainer="Muhammet Berdimyradov"

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev build-base
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "./main.py"]
