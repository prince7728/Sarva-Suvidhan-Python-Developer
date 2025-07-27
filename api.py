from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict
from sqlalchemy import create_engine, Column, Integer, String, Date, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:root7728@localhost:3306/kpa_forms"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# SQLAlchemy Models
class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"
    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String(50), nullable=False)
    submittedBy = Column(String(50), nullable=False)
    submittedDate = Column(String(20), nullable=False)
    fields = Column(Text, nullable=False)  # Store as JSON string

class BogieChecksheetDB(Base):
    __tablename__ = "bogie_checksheet"
    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String(50), nullable=False)
    inspectionBy = Column(String(50), nullable=False)
    inspectionDate = Column(String(20), nullable=False)
    bogieDetails = Column(Text, nullable=False)  # Store as JSON string
    bogieChecksheet = Column(Text, nullable=False)  # Store as JSON string
    bmbcChecksheet = Column(Text, nullable=False)  # Store as JSON string

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class WheelFields(BaseModel):
    treadDiameterNew: Optional[str] = None
    lastShopIssueSize: Optional[str] = None
    condemningDia: Optional[str] = None
    wheelGauge: Optional[str] = None
    variationSameAxle: Optional[str] = None
    variationSameBogie: Optional[str] = None
    variationSameCoach: Optional[str] = None
    wheelProfile: Optional[str] = None
    intermediateWWP: Optional[str] = None
    bearingSeatDiameter: Optional[str] = None
    rollerBearingOuterDia: Optional[str] = None
    rollerBearingBoreDia: Optional[str] = None
    rollerBearingWidth: Optional[str] = None
    axleBoxHousingBoreDia: Optional[str] = None
    wheelDiscWidth: Optional[str] = None

class WheelSpecRequest(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: str
    fields: WheelFields

class BogieDetails(BaseModel):
    bogieNo: Optional[str] = None
    makerYearBuilt: Optional[str] = None
    incomingDivAndDate: Optional[str] = None
    deficitComponents: Optional[str] = None
    dateOfIOH: Optional[str] = None

class BogieChecksheet(BaseModel):
    bogieFrameCondition: Optional[str] = None
    bolster: Optional[str] = None
    bolsterSuspensionBracket: Optional[str] = None
    lowerSpringSeat: Optional[str] = None
    axleGuide: Optional[str] = None

class BmbcChecksheet(BaseModel):
    cylinderBody: Optional[str] = None
    pistonTrunnion: Optional[str] = None
    adjustingTube: Optional[str] = None
    plungerSpring: Optional[str] = None

class BogieChecksheetRequest(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: str
    bogieDetails: BogieDetails
    bogieChecksheet: BogieChecksheet
    bmbcChecksheet: BmbcChecksheet

# POST: Wheel Specifications
@app.post("/forms/wheel-specifications")
def create_wheel_specification(data: WheelSpecRequest, db: Session = Depends(get_db)):
    db_obj = WheelSpecification(
        formNumber=data.formNumber,
        submittedBy=data.submittedBy,
        submittedDate=data.submittedDate,
        fields=json.dumps(data.fields.dict())
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return {
        "success": True,
        "message": "Wheel specification submitted successfully.",
        "data": {
            "formNumber": db_obj.formNumber,
            "submittedBy": db_obj.submittedBy,
            "submittedDate": db_obj.submittedDate,
            "status": "Saved"
        }
    }

# GET: Wheel Specifications
@app.get("/forms/wheel-specifications")
def get_wheel_specifications(
    formNumber: Optional[str] = Query(None),
    submittedBy: Optional[str] = Query(None),
    submittedDate: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(WheelSpecification)
    if formNumber:
        query = query.filter(WheelSpecification.formNumber == formNumber)
    if submittedBy:
        query = query.filter(WheelSpecification.submittedBy == submittedBy)
    if submittedDate:
        query = query.filter(WheelSpecification.submittedDate == submittedDate)
    results = query.all()
    data = []
    for item in results:
        data.append({
            "formNumber": item.formNumber,
            "submittedBy": item.submittedBy,
            "submittedDate": item.submittedDate,
            "fields": json.loads(item.fields)
        })
    return {
        "success": True,
        "message": "Filtered wheel specification forms fetched successfully.",
        "data": data
    }

# POST: Bogie Checksheet
@app.post("/forms/bogie-checksheet")
def create_bogie_checksheet(data: BogieChecksheetRequest, db: Session = Depends(get_db)):
    db_obj = BogieChecksheetDB(
        formNumber=data.formNumber,
        inspectionBy=data.inspectionBy,
        inspectionDate=data.inspectionDate,
        bogieDetails=json.dumps(data.bogieDetails.dict()),
        bogieChecksheet=json.dumps(data.bogieChecksheet.dict()),
        bmbcChecksheet=json.dumps(data.bmbcChecksheet.dict())
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return {
        "success": True,
        "message": "Bogie checksheet submitted successfully.",
        "data": {
            "formNumber": db_obj.formNumber,
            "inspectionBy": db_obj.inspectionBy,
            "inspectionDate": db_obj.inspectionDate,
            "status": "Saved"
        }
    }
