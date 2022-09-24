from logging import getLogger

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import registry, sessionmaker

from veterinary_clinic.db import start_mappers, set_up_db
from veterinary_clinic.service import VeterinaryClinic, UnitOfWork


logger = getLogger(__name__)


def bootstrap(
    db_uri: str,
) -> VeterinaryClinic:
    
    Session = sessionmaker(create_engine(db_uri, echo=True), expire_on_commit=False)

    mapper_registry = registry()
    try:
        start_mappers(mapper_registry)
    except ArgumentError:
        logger.warning("Mapper already exists.")
    set_up_db(db_uri, mapper_registry)

    uow = UnitOfWork(Session)

    return VeterinaryClinic(uow)