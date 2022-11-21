from enum import Enum
from typing import TypeVar
from dataclasses import dataclass, fields
from datetime import datetime


class ValidationError(Exception):
    pass

class PetType(str, Enum):
    DOG = "DOG"
    CAT = "CAT"

@dataclass
class Pet:
    type: PetType
    name: str

class AppointmentType(Enum):
    CHECK_UP = "CHECK_UP"
    OPERATION = "OPERATION"

@dataclass
class Appointment:
    type : AppointmentType
    datetime: datetime


T = TypeVar('T')


def dataclass_from_dict(klass: T, d) -> T:
    try:
        fieldtypes = {f.name:f.type for f in fields(klass)}
        return klass(**{f:dataclass_from_dict(fieldtypes[f],d[f]) for f in d})
    except:
        return d



def validate_schema(expected_schema: T, input_dict: dict) -> T:
    input_attr = dict()
    for attr, attr_type in expected_schema.__annotations__.items():
        try:
            if hasattr(attr_type, "__dict__"):
                input_attr[attr] = validate_schema(input_dict[attr])
            else:
                input_attr[attr] = attr_type(input_dict[attr])
        except:
            raise ValidationError
    return dataclass_from_dict(expected_schema, input_attr)