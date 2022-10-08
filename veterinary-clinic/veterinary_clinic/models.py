import time

from enum import Enum
from typing import Set
from datetime import datetime
from dataclasses import dataclass, field


class PetType(Enum):
    Cat = "Cat"
    Dog = "Dog"


class AppointmentType(Enum):
    CHECK_UP = "check_up"
    OPERATION = "operation"

@dataclass
class Appointment:
    id: str
    type: AppointmentType
    date: datetime
    
    def generate_report(self) -> str:
        match self.type:
            case AppointmentType.CHECK_UP:
                time.sleep(1)
                return "You're pet is not ill !"
            case AppointmentType.OPERATION:
                time.sleep(3)
                return "The operation has succefully ended."


@dataclass
class Pet:
    id: str
    name: str
    type: PetType
    appointments: Set[Appointment] = field(default_factory=set)

    def add_appointment(self, appointment: Appointment):
        self.appointments.add(appointment)

    def get_report(self, appointment_id: str):

        appointment = next((a for a in iter(self.appointments) if a.id==appointment_id), None)

        if not appointment:
            raise ValueError(f"No appointment found for id {appointment_id}")

        report = appointment.generate_report()

        match self.type:
            case PetType.CAT:
                return dict(
                    msg=f"Your cat {self.name} is healthy but hate you more than ever now. {report}")
            case PetType.DOG:
                return dict(
                    msg=f"Your dog {self.name} is healthy and is ready happy to see you. {report}")
