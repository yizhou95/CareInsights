from sqlalchemy import Column, String, BigInteger
from models import db

class Encounters(db.Model):
    __tablename__ = 'encounters'
    Id = Column(String(50), primary_key=True)
    START = Column(String(50))
    STOP = Column(String(50))
    PATIENT = Column(String(50))
    ORGANIZATION = Column(String(50))
    PROVIDER = Column(String(50))
    PAYER = Column(String(50))
    ENCOUNTERCLASS = Column(String(50))
    CODE = Column(String(10))
    DESCRIPTION = Column(String(150))
    db.Model_ENCOUNTER_COST = Column(String(50))
    TOTAL_CLAIM_COST = Column(String(50))
    PAYER_COVERAGE = Column(String(50))
    REASONCODE = Column(String(50))
    REASONDESCRIPTION = Column(String(150))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}