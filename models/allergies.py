from sqlalchemy import Column, String, BigInteger
from models import db

# Model for allergies table
class Allergies(db.Model):
    __tablename__ = 'allergies'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    START = Column(String(10))
    STOP = Column(String(50))
    PATIENT = Column(String(50), nullable=False)
    ENCOUNTER = Column(String(50))
    CODE = Column(BigInteger)
    SYSTEM1 = Column(String(20))
    DESCRIPTION = Column(String(50))
    TYPE = Column(String(50))
    CATEGORY = Column(String(50))
    DESCRIPTION1 = Column(String(50))
    SEVERITY1 = Column(String(50))
    DESCRIPTION2 = Column(String(50))
    SEVERITY2 = Column(String(50))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}