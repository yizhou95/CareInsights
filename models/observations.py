from sqlalchemy import Column, String, BigInteger
from models import db

class Observations(db.Model):
    __tablename__ = 'observations'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    DATE = Column(String(20))
    PATIENT = Column(String(50))
    ENCOUNTER = Column(String(50))
    CATEGORY = Column(String(20))
    CODE = Column(String(20))
    DESCRIPTION = Column(String(250))
    VALUE = Column(String(150))
    UNITS = Column(String(50))
    TYPE = Column(String(15))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}