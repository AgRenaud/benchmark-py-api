import uuid

from fastapi import APIRouter, Depends

from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.models import Appointment, Pet

from fastapi_example import schema
from fastapi_example.dependencies import clinic_service

router = APIRouter()


def create_uid() -> str:
    return str(uuid.uuid4())

@router.get('/health')
def healthcheck():
    return {
        "status": "up"
    }

@router.post('/pets/')
def add_pet(pet: schema.Pet, service: VeterinaryClinic=Depends(clinic_service)):
    uid = create_uid()
    new_pet = Pet(uid, pet.name, pet.type)
    service.add_pet(new_pet)
    return {"msg": f"You're pet has been added to the database with id: {uid}"}


@router.post('/pets/{pet_id}/appointments/')
def add_appointment(appointment: schema.Appointment, pet_id: str, service: VeterinaryClinic=Depends(clinic_service)):
    uid = create_uid()

    with service.uow as uow:
        new_appointment = Appointment(uid, appointment.type.value, appointment.datetime)
        service.add_appointment(pet_id, new_appointment)
    return {"msg": f"You're appointment for {new_appointment.date} has been added to the database with id: {uid}"}


@router.get('/pets/{pet_id}/appointments/{appointment_id}/report')
def download_report(appointment_id: str, service: VeterinaryClinic=Depends(clinic_service)):
    return service.get_report(appointment_id)