import time

from sqlalchemy.orm import Session

from veterinary_clinic import models


class UnitOfWork:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        return self.session()

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
            self.uow.session.add(pet)

    def add_appointment(self, pet_id, appointment: models.Appointment) -> dict:
        with self.uow:
            self.uow.session.get()

    def get_report(self, appointment_id: str) -> dict:
        
        with self.uow:
            appointment = self.uow.appointments.get(appointment_id)
            
            if appointment is None:
                raise ValueError("Appointment not found")
                
            return appointment.generate_report()

