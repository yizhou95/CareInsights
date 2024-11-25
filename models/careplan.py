from sqlalchemy import Column, String, BigInteger
from models import db

class CarePlans(db.Model):
    __tablename__ = 'careplans'
    Id = Column(String(50), primary_key=True)
    START = Column(String(50))
    STOP = Column(String(50))
    PATIENT = Column(String(50))
    ENCOUNTER = Column(String(50))
    CODE = Column(BigInteger)
    DESCRIPTION = Column(String(250))
    REASONCODE = Column(String(50))
    REASONDESCRIPTION = Column(String(250))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}