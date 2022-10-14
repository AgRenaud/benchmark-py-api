import datetime

from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    DateTime,
    Enum,
    Text,
    create_engine,
)
from sqlalchemy.orm import registry, relationship

from veterinary_clinic.models import PetType, Pet, AppointmentType, Appointment


def start_mappers(mapper_registry: registry):
    pets = Table(
        "pets",
        mapper_registry.metadata,
        Column("id", Text, primary_key=True),
        Column("name", Text),
        Column("type", Enum(PetType)),
        Column("updated_at",DateTime,default=datetime.datetime.now, onupdate=datetime.datetime.now),
        Column("created_at", DateTime, default=datetime.datetime.now),
    )

    appointments = Table(
        "appointments",
        mapper_registry.metadata,
        Column("id", Text, primary_key=True),
        Column("pet_id", ForeignKey("pets.id")),
        Column("type", Enum(AppointmentType)),
        Column("date", DateTime),
        Column("updated_at",DateTime,default=datetime.datetime.now, onupdate=datetime.datetime.now),
        Column("created_at", DateTime, default=datetime.datetime.now),
    )

    appointments_mapper = mapper_registry.map_imperatively(Appointment, appointments)
    pets_mapper = mapper_registry.map_imperatively(Pet, pets, properties={"appointments": relationship(appointments_mapper, collection_class=set)})

def set_up_db(uri: str, mapper_registry: registry) -> None:
    engine = create_engine(uri)
    mapper_registry.metadata.create_all(engine)
