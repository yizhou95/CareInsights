from sqlalchemy import Column, String, BigInteger
from models import db

class Conditions(db.Model):
    __tablename__ = 'conditions'
    ENCOUNTER = Column(String(50), primary_key=True)
    START = Column(String(50))
    STOP = Column(String(50))
    PATIENT = Column(String(50))
    CODE = Column(String(50))
    DESCRIPTION = Column(String(150)) 

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}