import uuid

from fastapi import APIRouter, Depends

from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.models import Appointment, Pet

from fastapi_gunicorn import schema
from fastapi_gunicorn.dependencies import clinic_service

router = APIRouter()


def create_uid() -> str:
    return str(uuid.uuid4())

@router.post('/pets/')
def add_pet(pet: schema.Pet, service: VeterinaryClinic=Depends(clinic_service)):
    uid = create_uid()
    new_pet = Pet(uid, pet.name, pet.type)
    service.add_pet(new_pet)
    return {"msg": f"You're pet has been added to the database with id: {uid}"}


@router.post('/appointments/')
def add_appointment(appointment: schema.Appointment, service: VeterinaryClinic=Depends(clinic_service)):
    uid = create_uid()

    with service.uow as uow:
        pet = uow.pets.get(appointment.pet_id)
    
    new_appointment = Appointment(uid, pet, appointment.type.value, appointment.datetime)
    service.add_pet(new_appointment)
    return {"msg": f"You're appointment for {new_appointment.date} has been added to the database with id: {uid}"}


@router.get('/appointments/report')
def download_report(report_id: str, service: VeterinaryClinic=Depends(clinic_service)):
    return service.get_report(report_id)