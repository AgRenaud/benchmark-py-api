import time

from enum import Enum
from datetime import datetime
from dataclasses import dataclass


class PetType(Enum):
    Cat = "Cat"
    Dog = "Dog"


@dataclass
class Pet:
    id: str
    name: str
    type: PetType

    def get_report(self):
        match self.type:
            case PetType.CAT:
                return dict(
                    msg=f"Your cat {self.name} is healthy but hate you more than ever now.")
            case PetType.DOG:
                return dict(
                    msg=f"Your dog {self.name} is healthy and is ready happy to see you.")



class AppointmentType(Enum):
    CHECK_UP = "check_up"
    OPERATION = "operation"


@dataclass
class Appointment:
    id: str
    pet: Pet
    type: AppointmentType
    date: datetime
    
    def generate_report(self):
        match self.type:
            case AppointmentType.CHECK_UP:
                time.sleep(1)
            case AppointmentType.OPERATION:
                time.sleep(3)

        return self.pet.get_report()