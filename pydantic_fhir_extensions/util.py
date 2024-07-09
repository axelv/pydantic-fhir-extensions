
from pydantic import SerializationInfo


def is_serialization_to_fhir(info:SerializationInfo):
    return bool(info.context is not None and info.context.get("fhir", False) == True)
