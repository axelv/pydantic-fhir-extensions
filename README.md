# FHIR Extensions as Python properties

This repository is a POC that demonstrates how you can access [FHIR extensions] as Python properties when utilizing Pydantic as FHIR/JSON validation engine.

Using simple type annotations, the extensions on FHIR Elements are automatically validated and converted to Python properties.

## Example code

Model definition:

```python
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
```

Example validation code:

```python
fhir_json = {
    "extension": [
        {
            "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
            "valueCodeableConcept": {
                "text": "Text Area",
                "coding": [
                    {
                        "system": "http://tiro.health/fhir/CodeSystem/tiro-questionnaire-item-control",
                        "code": "text-area",
                        "display": "Text Area"
                    }
                ]
            }
        }
    ],
    "type": "text",
    "text": "This is a question",
    "linkId": "question-1.1"
}

result = QuestionnaireItem.model_validate(json_1)
assert result.itemControl.code == "text-area"
assert result.itemControl.display == "Text Area"
assert len(result.extension) == 1
```
