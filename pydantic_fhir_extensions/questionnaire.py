
from typing import Annotated, List, Literal

from pydantic_fhir_extensions.element import BaseElement
from pydantic_fhir_extensions.base import Coding
from pydantic_fhir_extensions.extensions import ExtItemControl, ExtAnswerOptionsToggleExpression
from pydantic_fhir_extensions.extensions.validator import ExtensionValidator

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
