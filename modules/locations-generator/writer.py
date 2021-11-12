import time
import grpc
import location_pb2
import location_pb2_grpc
import logging, sys

def writer():
    """
    Assume we get raw location data from sensors, normalize it in compliance with DB table records and finally send in a message,
    this function manually generates dummy 5 location_id's from  id 100 to 105
    """

    channel = grpc.insecure_channel("localhost:5005")
    stub = location_pb2_grpc.LocationServiceStub(channel)

    for i in range(100,106):
        location = location_pb2.LocationMessage(
            id=i,
            person_id=9,
            longitude="-106.5719566",
            latitude="35.0585136",
            creation_time="2021-11-06T10:10:10"
        )
        response = stub.Create(location)
        logger.info("Location with location_id=" + str(i) + " was sent")

# Some logging stuff
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdouth = logging.StreamHandler(sys.stdout)
stdouth.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s, %(message)s', datefmt='%m/%d/%Y, %H:%M:%S')
stdouth.setFormatter(formatter)
logger.addHandler(stdouth)

# Keep thread alive
while True:
    writer()
    time.sleep(86400)