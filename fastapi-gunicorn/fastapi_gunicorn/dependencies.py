
from veterinary_clinic.service import VeterinaryClinic
from veterinary_clinic.bootstrap import bootstrap


def clinic_service(uri: str="sqlite:///local.sqlite3") -> VeterinaryClinic:
    return bootstrap(uri)