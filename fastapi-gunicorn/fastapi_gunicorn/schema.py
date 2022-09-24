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
    CHECK_UP = "check_up"
    OPERATION = "operation"

class Appointment(BaseModel):
    pet_id: str
    type : AppointmentType
    datetime: datetime
