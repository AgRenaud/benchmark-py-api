
from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.bootstrap import bootstrap


def clinic_service() -> VeterinaryClinic:
    return bootstrap("sqlite:///local.sqlite3")