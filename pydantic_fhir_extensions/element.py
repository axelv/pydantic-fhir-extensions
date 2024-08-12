
from itertools import filterfalse
from typing import Any, List, Sequence
from pydantic import BaseModel, SerializationInfo, field_serializer, model_serializer
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from pydantic_fhir_extensions.base import BaseExtension
from pydantic_fhir_extensions.extensions.validator import find_extension_validator
from pydantic_fhir_extensions.util import is_serialization_to_fhir


class BaseElement(BaseModel):
    extension: SkipJsonSchema[Sequence["BaseExtension"]] = Field(default_factory=list)

    @field_serializer("extension", when_used="always")
    def serialize_extension(self, value:List["BaseExtension"], info:SerializationInfo):
        to_fhir = is_serialization_to_fhir(info)
        if not to_fhir:
            return value
        extension:List[BaseExtension] = [*value]
        for field_name, ext_validator in self.iter_extension_fields():
            # remove attribute extensions from the list of extensions
            extension = list(filterfalse(ext_validator.match, extension))
        return extension

    @classmethod
    def iter_extension_fields(cls):
        """ Iterate over the fields that are extensions """
        for field_name, field_info in cls.model_fields.items():
            maybe_ext_validator = find_extension_validator(field_info.metadata)
            if maybe_ext_validator is not None:
                yield field_name, maybe_ext_validator

    def model_dump_fhir(self):
        exclude_fields = {field_name for field_name, _ in self.iter_extension_fields()}
        return self.model_dump(mode="json", context={"fhir":True}, exclude_none=True, exclude=exclude_fields)

    @field_serializer("*", when_used="always")
    def serialize_fhir(self, value:Any, info:SerializationInfo):
        to_fhir = is_serialization_to_fhir(info)
        if to_fhir and is_empty_sequence(value):
            return None
        return value

def is_empty_sequence(value:Any)->bool:
    if isinstance(value, (tuple, list, set)) and len(value):
        return True
    return False
