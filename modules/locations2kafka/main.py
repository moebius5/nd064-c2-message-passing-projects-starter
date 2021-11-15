import json
import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
import logging, sys

from kafka import KafkaProducer
from grpc_reflection.v1alpha import reflection

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        logger.info("Received new location")
        location_value = {
            "id": request.id,
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time
        }
        print(location_value)
        producer.send(TOPIC_NAME, location_value)
        producer.flush()
        logger.info("Location data was sent to Kafka")
        return location_pb2.LocationMessage(**location_value)


# Some logging stuff
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdouth = logging.StreamHandler(sys.stdout)
stdouth.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s, %(message)s', datefmt='%m/%d/%Y, %H:%M:%S')
stdouth.setFormatter(formatter)
logger.addHandler(stdouth)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

# enabling reflection service
SERVICE_NAMES = (
    location_pb2.DESCRIPTOR.services_by_name['LocationServicer'].full_name,
    reflection.SERVICE_NAME,
)
reflection.enable_server_reflection(SERVICE_NAMES, server)

logger.info("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

