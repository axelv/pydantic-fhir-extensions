
from typing import List, Literal, Self, Sequence
from pydantic import BaseModel, Field, ValidationInfo, field_validator

from pydantic_fhir_extensions.base import BaseElement, Coding


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

def map_item_control_coding_to_codeable_concept(coding: Coding) -> ItemControlCodeableConcept:
    """ Map an item control coding to a codeable concept """

    match coding:
        case Coding(system=TIRO_ITEM_CONTROL_SYSTEM, code="text", display=display):
            return ItemControlCodeableConcept(
                text="Text",
                coding=[coding]
            )
        case Coding(system=TIRO_ITEM_CONTROL_SYSTEM, code="radio", display=display):
            return ItemControlCodeableConcept(
                text="Radio",
                coding=[coding],
            )
        case Coding(system=TIRO_ITEM_CONTROL_SYSTEM, code="checkbox", display=display):
            return ItemControlCodeableConcept(
                text="Checkbox",
                coding=[coding],
            )
        case Coding(system=TIRO_ITEM_CONTROL_SYSTEM, code="dropdown", display=display):
            return ItemControlCodeableConcept(
                text="Dropdown",
                coding=[coding],
            )
        case Coding(system=TIRO_ITEM_CONTROL_SYSTEM, code="text-area", display=display):
            return ItemControlCodeableConcept(
                text="Text Area",
                coding=[coding],
            )
        case _:
            raise ValueError(f"Item control code `{coding.system}|{coding.code}` not recognized")

    raise ValueError('No item control code found')


def map_item_control_codeable_concept_to_coding(concept: ItemControlCodeableConcept) -> Coding:
    """ Extract the Tiro.health item control coding from a codeable concept """

    for coding in concept.coding:
        match coding:
            case Coding(system=TIRO_ITEM_CONTROL_SYSTEM, code=code, display=display):
                return coding
    raise ValueError('No item control code found')

class ExtItemControl(BaseElement):
    url: Literal["http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl"] = Field(default="http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl", frozen=True)
    valueCodeableConcept: ItemControlCodeableConcept

    @classmethod
    def to_property_value(cls, *extensions:Self):
        assert len(extensions) == 1, "Only one item control extension is allowed"
        return map_item_control_codeable_concept_to_coding(extensions[0].valueCodeableConcept)

    @classmethod
    def from_property_value(cls, value:Coding):
        yield cls(valueCodeableConcept=map_item_control_coding_to_codeable_concept(value))
