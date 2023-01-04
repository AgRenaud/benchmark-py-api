import uuid

from flask import Blueprint, request

from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.models import Appointment, Pet

from flask_example import schema
from flask_example.dependencies import clinic_service



def create_uid() -> str:
    return str(uuid.uuid4())


class  ClinicController:

    blueprint = Blueprint("ClinicController", __name__)

    def __init__(self, service: VeterinaryClinic=clinic_service()) -> None:
        self.service = service
        self.__init_enpoints__()

    def __init_enpoints__(self):
        self.blueprint.add_url_rule('/health', 'health', self.healthcheck, methods=['GET'])
        self.blueprint.add_url_rule('/pets/', 'pets', self.add_pet, methods=['POST'])
        self.blueprint.add_url_rule('/pets/<pet_id>/appointments', 'appointments', self.add_appointment, methods=['POST'])
        self.blueprint.add_url_rule('/pets/<pet_id>/appointments/<appointment_id>/report', 'report', self.download_report, methods=['GET'])

    def healthcheck(self):
        return {
            "status": "up"
        }

    def add_pet(self):
        request_data = request.json
        pet = schema.validate_schema(schema.Pet, request_data)

        uid = create_uid()
        new_pet = Pet(uid, pet.name, pet.type)
        self.service.add_pet(new_pet)
        return {
            "id": uid,
            "msg": f"You're pet has been added to the database with id: {uid}"
        }

    def add_appointment(self, pet_id: str):
        request_data = request.json
        appointment = schema.validate_schema(schema.Appointment, request_data)

        uid = create_uid()
        with self.service.uow as uow:
            new_appointment = Appointment(uid, appointment.type.value, appointment.datetime)
            self.service.add_appointment(pet_id, new_appointment)
        return {"msg": f"You're appointment for {new_appointment.date} has been added to the database with id: {uid}"}

    def download_report(self, appointment_id: str):
        return self.service.get_report(appointment_id)