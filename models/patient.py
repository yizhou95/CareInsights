from sqlalchemy import Column, String, BigInteger
from models import db

class Patients(db.Model):
    __tablename__ = 'patients'
    Id = Column(String(50), primary_key=True)
    BIRTHDATE = Column(String(50))
    DEATHDATE = Column(String(50))
    SSN = Column(String(20))
    DRIVERS = Column(String(20))
    PASSPORT = Column(String(20))
    PREFIX = Column(String(10))
    FIRST = Column(String(20))
    LAST = Column(String(20))
    SUFFIX = Column(String(10))
    MAIDEN = Column(String(20))
    MARITAL = Column(String(5))
    RACE = Column(String(10))
    ETHNICITY = Column(String(20))
    GENDER = Column(String(5))
    BIRTHPLACE = Column(String(100))
    ADDRESS = Column(String(50))
    CITY = Column(String(50))
    STATE = Column(String(50))
    COUNTY = Column(String(50))
    ZIP = Column(String(20))
    LAT = Column(String(20))
    LON = Column(String(20))
    HEALTHCARE_EXPENSES = Column(String(20))
    HEALTHCARE_COVERAGE = Column(String(20))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}