
from decimal import Decimal
from itertools import filterfalse
from typing import Any, Generic, Iterable, List, Literal, Self, Sequence, TypeVar
from typing_extensions import Annotated

from pydantic import BaseModel, Field, SerializationInfo, StringConstraints, field_serializer, field_validator, model_validator
from pydantic.functional_serializers import model_serializer

from pydantic_fhir_extensions.extension_validator import ExtensionValidator, Extension, TUrl
from pydantic_fhir_extensions.util import is_serialization_to_fhir

id = Annotated[str, StringConstraints(pattern=r"[A-Za-z0-9\-\.]{1,64}")]

class Coding(BaseModel):
    system:str
    code:str
    display:str | None = None
    userSelected:bool | None = None
    version:str | None = None

    model_config = {"frozen": True}

    def __hash__(self):
        if self.version is not None:
            return hash((self.system, self.code, self.version))
        return hash((self.system, self.code))

class CodeableConcept(BaseModel):
    text: str
    coding: Sequence[Coding] = Field(default_factory=list)

class Expression(BaseModel):
    description: str | None = None
    expression: str
    name: id | None = None
    language: Literal["text/fhirpath"] = "text/fhirpath"

class BaseExtension(BaseModel):
    extension: List["BasePropertyExtension"] = Field(default_factory=list)
    url:str
    valueString: str | None = None
    valueCoding: Coding | None = None
    valueCodeableConcept: CodeableConcept | None = None
    valueDecimal: Decimal | None = None
    valueInteger: int | None = None
    valueBoolean: bool | None = None
    valueExpression: Expression | None = None
    """
    @model_validator(mode="before")
    def at_most_one_value(self, data: Any):
        if not isinstance(data, dict):
            return data
        assert sum(1 for field_name, value in data.items() if field_name.startswith("value")) <= 1, "Only one value type is allowed"
        return data
    """

def make_list(value:Any):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

class BaseElement(BaseModel):
    extension: List[BasePropertyExtension] = Field(default_factory=list)

    @field_serializer("extension")
    def serialize_extension(self, value:List[BasePropertyExtension], info:SerializationInfo):
        to_fhir = is_serialization_to_fhir(info)
        extension:List[Extension] = [*value]
        for field_name, ext_validator in self.iter_extension_fields():
            # remove attribute extensions from the list of extensions
            extension = list(filterfalse(ext_validator.match, extension))
            if to_fhir: # add attribute extensions as class FHIR extensions
                extension.extend(ext_validator.extension_model.from_property_value(make_list(getattr(self, field_name))))
        return extension

    @classmethod
    def iter_extension_fields(cls):
        for field_name, field_info in cls.model_fields.items():
            maybe_ext_validator = find_extension_validator(field_info.metadata)
            if maybe_ext_validator is not None:
                yield field_name, maybe_ext_validator

    def model_dump_fhir(self):
        exclude_fields = {field_name for field_name, _ in self.iter_extension_fields()}
        return self.model_dump(mode="json", context={"fhir":True}, exclude_none=True, exclude=exclude_fields)

TUrl = TypeVar("TUrl", bound=str)

def find_extension_validator(metadata:List[Any])->ExtensionValidator|None:
    for meta in metadata:
        if isinstance(meta, ExtensionValidator):
            return meta
    return None
