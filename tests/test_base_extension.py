from pydantic import ValidationError
import pytest

from pydantic_fhir_extensions.base import BaseExtension

def test_if_value_and_nested_extension_fails():
    json = {
        "url": "test-uri",
        "extension": [
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression",
                "valueCoding": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "yes",
                    "display": "Yes"
                }
            }
        ],
        "valueExpression": {
            "description": "This is a description",
            "language": "text/fhirpath",
            "expression": "This is an expression"
        }
    }

    with pytest.raises(ValidationError):
        BaseExtension.model_validate(json)

def test_if_multiple_values_fail():
    json = {
        "url": "test-uri",
        "valueCoding": {
            "system": "urn:CodeSystem:toggle",
            "code": "yes",
            "display": "Yes"
        },
        "valueString": "This is a string"
    }

    with pytest.raises(ValidationError):
        BaseExtension.model_validate(json)
