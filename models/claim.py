from sqlalchemy import Column, String, BigInteger
from models import db

class ClaimsTransactions(db.Model):
    __tablename__ = 'claims_transactions'
    ID = Column(String(50), primary_key=True)
    CLAIMID = Column(String(50))
    CHARGEID = Column(String(50))
    PATIENTID = Column(String(50))
    TYPE = Column(String(50))
    AMOUNT = Column(String(50))
    METHOD = Column(String(50))
    FROMDATE = Column(String(50))
    TODATE = Column(String(50))
    PLACEOFSERVICE = Column(String(50))
    PROCEDURECODE = Column(String(50))
    DEPARTMENTID = Column(String(50))
    NOTES = Column(String(250))
    UNITAMOUNT = Column(String(50))
    TRANSFEROUTID = Column(String(50))
    TRANSFERTYPE = Column(String(50))
    PAYMENTS = Column(String(50))
    TRANSFERS = Column(String(50))
    OUTSTANDING = Column(String(50))
    APPOINTMENTID = Column(String(50))
    LINENOTE = Column(String(50))
    PATIENTINSURANCEID = Column(String(50))
    PROVIDERID = Column(String(50))
    SUPERVISINGPROVIDERID = Column(String(50))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}