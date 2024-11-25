from sqlalchemy import Column, String, BigInteger
from models import db

class Providers(db.Model):
    __tablename__ = 'providers'
    Id = Column(String(50), primary_key=True)
    ORGANIZATION = Column(String(50))
    NAME = Column(String(50))
    GENDER = Column(String(5))
    SPECIALITY = Column(String(50))
    ADDRESS = Column(String(50))
    CITY = Column(String(20))
    STATE = Column(String(5))
    ZIP = Column(String(20))
    LAT = Column(String(20))
    LON = Column(String(20))
    UTILIZATION = Column(String(20))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}