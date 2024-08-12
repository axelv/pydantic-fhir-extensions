
from decimal import Decimal
from typing import Any, List, Literal, Sequence
from typing_extensions import Annotated

from pydantic import BaseModel, Field, StringConstraints, model_validator
from pydantic.json_schema import SkipJsonSchema


id = Annotated[str, StringConstraints(pattern=r"[A-Za-z0-9\-\.]{1,64}")]
canonical = Annotated[str, StringConstraints(pattern=r"\S*")]

DATE_PATTERN = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1]))?)?"
date = Annotated[str, StringConstraints(pattern=DATE_PATTERN)]

DATETIME_PATTERN = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]{1,9})?)?)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)?)?)?"
dateTime = Annotated[str, StringConstraints(pattern=DATETIME_PATTERN)]

class Quantity(BaseModel):
    value: Decimal
    unit: str
    code: str
    system: str

class Coding(BaseModel):
    code:str
    system:str | None = None
    display:str | None = None
    userSelected:bool | None = None
    version:str | None = None

    def __hash__(self):
        if self.version is not None:
            return hash((self.system, self.code, self.version))
        return hash((self.system, self.code))

    def __eq__(self, other):
        if isinstance(other, Coding):
            return self.system == other.system and self.code == other.code and self.version == other.version
        return False

class CodeableConcept(BaseModel):
    text: str
    coding: Sequence[Coding] = Field(default_factory=list)

class Expression(BaseModel):
    description: str | None = None
    expression: str
    name: id | None = None
    language: Literal["text/fhirpath"] = "text/fhirpath"

class BaseExtension(BaseModel):
    extension: SkipJsonSchema[List["BaseExtension"]] = Field(default_factory=list)
    url:str
    valueString: str | None = None
    valueCoding: Coding | None = None
    valueCodeableConcept: CodeableConcept | None = None
    valueDecimal: Decimal | None = None
    valueInteger: int | None = None
    valueBoolean: bool | None = None
    valueExpression: Expression | None = None

    @model_validator(mode="after")
    def at_most_one_value(self):
        assert sum(1 for field_name in self.model_fields_set if field_name.startswith("value") and getattr(self,field_name) is not None) <= 1, "Only one value type is allowed"
        return self

    @model_validator(mode="after")
    def either_values_or_extension(self):
        has_value = any(getattr(self, field_name) is not None for field_name in self.model_fields_set if field_name.startswith("value"))
        has_extension = len(self.extension) > 0
        if has_value and has_extension:
            raise ValueError("Either value or extension can be present, not both")
        return self
