FROM python:3.8-alpine
LABEL maintainer="Muhammet Berdimyradov"
WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers libc-dev
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto

COPY . .
CMD ["python", "./writer.py"]