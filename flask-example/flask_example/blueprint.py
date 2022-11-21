import uuid

from flask import Blueprint

from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.models import Appointment, Pet

from flask_example.dependencies import clinic_service



def create_uid() -> str:
    return str(uuid.uuid4())


class  ClinicController:
    Blueprint = Blueprint("clinic")

    def __init__(self, service: VeterinaryClinic) -> None:
        self.service = service


    @blueprint.post('/pets/')
    def add_pet(self, pet: schema.Pet):
        uid = create_uid()
        new_pet = Pet(uid, pet.name, pet.type)
        self.service.add_pet(new_pet)
        return {"msg": f"You're pet has been added to the database with id: {uid}"}


    @blueprint.post('/pets/{pet_id}/appointments/')
    def add_appointment(self, appointment: schema.Appointment, pet_id: str):
        uid = create_uid()

        with service.uow as uow:
            new_appointment = Appointment(uid, appointment.type.value, appointment.datetime)
            self.service.add_appointment(pet_id, new_appointment)
        return {"msg": f"You're appointment for {new_appointment.date} has been added to the database with id: {uid}"}


    @blueprint.get('/pets/{pet_id}/appointments/{appointment_id}/report')
    def download_report(self, appointment_id: str):
        return self.service.get_report(appointment_id)