import time

from sqlalchemy.orm import Session

from veterinary_clinic import models


class PetRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, pet: models.Pet) -> None:
        if self.get(pet.id):
            raise ValueError('Pet already exists')
        self.session.add(pet)

    def get(self, id: str) -> models.Pet | None:
        pet = self.session.query(models.Pet).filter_by(id=id).first()
        return pet


class AppointmentRepository:
    def __init__(self, session: Session, pets: PetRepository) -> None:
        self.session = session
        self.pets = pets

    def add(self, appointment: models.Appointment) -> None:
        if self.get(appointment.id):
            raise ValueError("Appointment already exists")
        if self.pets.get(appointment.pet) is None:
            raise ValueError("Pet does not exist")
        self.session.add(appointment)

    def get(self, id: str) -> models.Appointment | None:
        appointment = self.session.query(models.Appointment).filter_by(id=id).first()
        return appointment


class UnitOfWork:

    pets: PetRepository
    appointments: AppointmentRepository

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.pets = PetRepository(self.session)
        self.appointments = AppointmentRepository(self.session, self.pets)
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class VeterinaryClinic:
    """
    All the services of your awesome Veterinary Clinic are implemented here.

    Here you can manage your pet book by adding pet to your database.
    You're also able to add new appointments for any pet in your database.

    There is also a service that send you a report about your pet appointment.
    The generation of the report depends on the Pet and the appointment type
    """

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add_pet(self, pet: models.Pet) -> dict:
        with self.uow:
            self.uow.pets.add(pet)

    def add_appointment(self, appointment: models.Appointment) -> dict:
        with self.uow:
            self.uow.appointments.add(appointment)

    def get_report(self, appointment_id: str) -> dict:
        
        with self.uow:
            appointment = self.uow.appointments.get(appointment_id)
            
            if appointment is None:
                raise ValueError("Appointment not found")
                
            return appointment.generate_report()

