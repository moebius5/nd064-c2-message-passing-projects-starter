import logging
from datetime import datetime, timedelta
from typing import Dict, List

#######from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import *

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

#engine = create_engine('postgresql://ct_admin:wowimsosecure@localhost:32543/geoconnections')
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)
session = Session()

class LocationService:
    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.id = location["id"]
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session.add(new_location)
        session.commit()

        return new_location


