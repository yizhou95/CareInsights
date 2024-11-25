from sqlalchemy import Column, String, BigInteger
from models import db

class Procedures(db.Model):
    __tablename__ = 'procedures'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    START = Column(String(20))
    STOP = Column(String(20))
    PATIENT = Column(String(50))
    ENCOUNTER = Column(String(50))
    CODE = Column(String(20))
    DESCRIPTION = Column(String(250))
    db.Model_COST = Column(String(20))
    REASONCODE = Column(String(20))
    REASONDESCRIPTION = Column(String(150))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}