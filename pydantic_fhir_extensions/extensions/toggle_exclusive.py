

from typing import Annotated, Literal, Self, Sequence

from pydantic import Field
from pydantic_fhir_extensions.extension_validator import ExtensionValidator
from pydantic_fhir_extensions.base import BaseElement, Coding, Expression


ANSWER_OPTION_TOGGLE_EXPRESSION = "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression"

class ExtOption(BaseElement):
    url: Literal["option"] = Field(default="option", frozen=True)
    valueCoding: Coding

    @classmethod
    def from_property_value(cls, value:Coding):
        yield cls(valueCoding=value)

    @classmethod
    def to_property_value(cls, *extension:Self):
        assert len(extension) == 1
        return extension[0].valueCoding

class ExtToggleExpression(BaseElement):
    url: Literal["expression"] = Field(default="expression", frozen=True)
    valueExpression: Expression

    @classmethod
    def from_property_value(cls, value:Expression):
        yield cls(valueExpression=value)

    @classmethod
    def to_property_value(cls, *extension:Self):
        assert len(extension) == 1
        return extension[0].valueExpression

class ExtAnswerOptionsToggleExpression(BaseElement):
    url: Literal["http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression"] = Field(default="http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression", frozen=True)
    option: Annotated[Coding, ExtensionValidator(ExtOption)]
    expression: Annotated[Expression, ExtensionValidator(ExtToggleExpression)]

    @classmethod
    def from_property_value(cls, items:Sequence[Self]):
        yield from items

    @classmethod
    def to_property_value(cls, *items:Self)->Sequence[Self]:
        return items
