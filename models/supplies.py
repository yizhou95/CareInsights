from sqlalchemy import Column, String, BigInteger
from models import db

class Supplies(db.Model):
    __tablename__ = 'supplies'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    DATE = Column(String(20))
    PATIENT = Column(String(50))
    ENCOUNTER = Column(String(50))
    CODE = Column(String(20))
    DESCRIPTION = Column(String(250))
    QUANTITY = Column(String(20))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}