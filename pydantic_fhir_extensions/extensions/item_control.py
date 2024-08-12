
from typing import List, Literal, Self, Sequence
from pydantic import Field, ValidationInfo, field_validator

from pydantic_fhir_extensions.element import BaseElement
from pydantic_fhir_extensions.base import Coding
from pydantic_fhir_extensions.extensions.validator import ValidateableExtension


class ItemControlCodeableConcept(BaseElement):
    text: str
    coding: List[Coding] = Field(default_factory=list, min_length=1)

    @field_validator("coding")
    @classmethod
    def at_least_answer_control_code(cls, v: Sequence[Coding], info:ValidationInfo):
        assert any(
            coding.system == TIRO_ITEM_CONTROL_SYSTEM
            for coding in v
        ), "At least one coding must be from the TIRO answer control system"
        return v
TIRO_ITEM_CONTROL_SYSTEM = "http://tiro.health/fhir/CodeSystem/tiro-questionnaire-item-control"
SDC_ITEM_CONTROL_SYSTEM = "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl"

TiroItemControl = Literal["text", "radio", "checkbox", "dropdown", "text-area"]

def map_item_control_coding_to_codeable_concept(code:str) -> ItemControlCodeableConcept:
    """ Map an item control coding to a codeable concept """

    match code:
        case "text":
            return ItemControlCodeableConcept(
                text="Text",
                coding=[
                    Coding(
                        system=TIRO_ITEM_CONTROL_SYSTEM,
                        code="text",
                        display="Text"
                    )
                ]
            )
        case "radio":
            return ItemControlCodeableConcept(
                text="Radio",
                coding=[
                    Coding(
                        system=TIRO_ITEM_CONTROL_SYSTEM,
                        code="radio",
                        display="Radio"
                    )
                ],
            )
        case "checkbox":
            return ItemControlCodeableConcept(
                text="Checkbox",
                coding=[
                    Coding(
                        system=TIRO_ITEM_CONTROL_SYSTEM,
                        code="checkbox",
                        display="Checkbox"
                    )
                ],
            )
        case "dropdown":
            return ItemControlCodeableConcept(
                text="Dropdown",
                coding=[
                    Coding(
                        system=TIRO_ITEM_CONTROL_SYSTEM,
                        code="dropdown",
                        display="Dropdown"
                    )
                ],
            )
        case "text-area":
            return ItemControlCodeableConcept(
                text="Text Area",
                coding=[
                    Coding(
                        system=TIRO_ITEM_CONTROL_SYSTEM,
                        code="text-area",
                        display="Text Area"
                    )
                ],
            )
        case _:
            raise ValueError(f"Item control code `{code}` not recognized")

    raise ValueError('No item control code found')


def map_item_control_codeable_concept_to_coding(concept: ItemControlCodeableConcept) -> str:
    """ Extract the Tiro.health item control coding from a codeable concept """

    for coding in concept.coding:
        match coding:
            case Coding(system="http://tiro.health/fhir/CodeSystem/tiro-questionnaire-item-control", code=code, display=_):
                return code
    raise ValueError('No item control code found')

class ExtItemControl(BaseElement):
    url: Literal["http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl"] = Field(default="http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl", frozen=True)
    valueCodeableConcept: ItemControlCodeableConcept

    @classmethod
    def to_property_value(cls, *extensions:Self):
        assert len(extensions) == 1, "Exactly one item control extension is allowed, but got %s" % len(extensions)
        return map_item_control_codeable_concept_to_coding(extensions[0].valueCodeableConcept)

    @classmethod
    def from_property_value(cls, value:str):
        yield cls(valueCodeableConcept=map_item_control_coding_to_codeable_concept(value))
