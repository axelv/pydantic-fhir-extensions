
from typing import Annotated, List, Literal

from pydantic_fhir_extensions.base import BaseElement, CodeableConcept, Coding, Expression
from pydantic_fhir_extensions.extension_validator import ExtensionValidator
from pydantic_fhir_extensions.extensions import ExtItemControl, ExtAnswerOptionsToggleExpression

class AnswerOption(BaseElement):
    valueCoding: Coding

QuestionnaireItemType = Literal["group", "coding", "display", "question", "boolean", "decimal", "integer", "date", "dateTime", "time", "string", "text", "url", "coding" "attachment", "reference", "quantity"]

class QuestionnaireItem(BaseElement):
    linkId: str
    text: str
    type: QuestionnaireItemType
    itemControl: Annotated[Coding, ExtensionValidator(ExtItemControl)]
    answerOption: List[AnswerOption]|None = None
    answerOptionsToggleExpression: Annotated[List[ExtAnswerOptionsToggleExpression], ExtensionValidator(ExtAnswerOptionsToggleExpression)]
