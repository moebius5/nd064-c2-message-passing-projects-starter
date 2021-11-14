FROM python:3.7-alpine
LABEL maintainer="Muhammet Berdimyradov"

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN pip install -r requirements.txt

EXPOSE 30001

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0", "--port 30001"]
