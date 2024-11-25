from sqlalchemy import Column, String, BigInteger
from models import db

class Immunizations(db.Model):
    __tablename__ = 'immunizations'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    DATE = Column(String(20))
    PATIENT = Column(String(50), nullable=False)
    ENCOUNTER = Column(String(50))
    CODE = Column(String(20))
    DESCRIPTION = Column(String(250))
    db.Model_COST = Column(String(20))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}