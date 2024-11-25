from sqlalchemy import Column, String, BigInteger
from models import db

class Organizations(db.Model):
    __tablename__ = 'organizations'
    Id = Column(String(50), primary_key=True)
    NAME = Column(String(100))
    ADDRESS = Column(String(50))
    CITY = Column(String(50))
    STATE = Column(String(10))
    ZIP = Column(String(20))
    LAT = Column(String(20))
    LON = Column(String(20))
    PHONE = Column(String(50))
    REVENUE = Column(String(20))
    UTILIZATION = Column(String(20))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}