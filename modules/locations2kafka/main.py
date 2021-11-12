import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
import logging, sys

from kafka import KafkaProducer

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'localhost:9092'

#producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        #print("Received a message!")
        logger.info("Received a message!")
        location_value = {
            "id": request.id,
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time
        }
        print(location_value)
        return location_pb2.LocationMessage(**location_value)

        #producer.send(TOPIC_NAME, b'location_value')
        #producer.flush()


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


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

