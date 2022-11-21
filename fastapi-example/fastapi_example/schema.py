from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class PetType(str, Enum):
    DOG = "DOG"
    CAT = "CAT"


class Pet(BaseModel):
    type: PetType
    name: str

class AppointmentType(Enum):
    CHECK_UP = "CHECK_UP"
    OPERATION = "OPERATION"

class Appointment(BaseModel):
    type : AppointmentType
    datetime: datetime
