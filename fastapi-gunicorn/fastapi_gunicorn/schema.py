from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class PetType(str, Enum):
    Dog = "Dog"
    Cat = "Cat"


class Pet(BaseModel):
    type: PetType
    name: str

class AppointmentType(Enum):
    check_up = "check_up"
    operation = "operation"

class Appointment(BaseModel):
    type : AppointmentType
    datetime: datetime
