import json

import logging, sys
from kafka import KafkaConsumer
from app.udaconnect.services import LocationService


KAFKA_SERVER = 'kafka:9092'
TOPIC_NAME = 'locations'


def main():
    while True:
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe([TOPIC_NAME])
        try:
            for message in consumer:
                location=message.value
                LocationService.create(location)
                logger.info("Location data:" + str(location) + "saved to database.")
        except KeyboardInterrupt:
            consumer.unsubscribe()
            consumer.close()

# Some logging stuff
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdouth = logging.StreamHandler(sys.stdout)
stdouth.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s, %(message)s', datefmt='%m/%d/%Y, %H:%M:%S')
stdouth.setFormatter(formatter)
logger.addHandler(stdouth)


if __name__ == "__main__":
    main()
