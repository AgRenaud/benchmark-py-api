import uuid

from flask import Blueprint, request

from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.models import Appointment, Pet

from flask_example import schema
from flask_example.dependencies import clinic_service



def create_uid() -> str:
    return str(uuid.uuid4())


class  ClinicController:

    blueprint = Blueprint("clinic")

    def __init__(self, service: VeterinaryClinic=clinic_service()) -> None:
        self.service = service


    @blueprint.post('/pets/')
    def add_pet(self):
        request_data = request.json
        pet = schema.validate_schema(schema.Pet, request_data)

        uid = create_uid()
        new_pet = Pet(uid, pet.name, pet.type)
        self.service.add_pet(new_pet)
        return {"msg": f"You're pet has been added to the database with id: {uid}"}


    @blueprint.post('/pets/<pet_id>/appointments/')
    def add_appointment(self, pet_id: str):
        request_data = request.json
        appointment = schema.validate_schema(schema.Appointment, request_data)

        uid = create_uid()
        with self.service.uow as uow:
            new_appointment = Appointment(uid, appointment.type.value, appointment.datetime)
            self.service.add_appointment(pet_id, new_appointment)
        return {"msg": f"You're appointment for {new_appointment.date} has been added to the database with id: {uid}"}


    @blueprint.get('/pets/<pet_id>/appointments/<appointment_id>/report')
    def download_report(self, appointment_id: str):
        return self.service.get_report(appointment_id)