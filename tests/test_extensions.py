

from pydantic_fhir_extensions.extensions import ExtAnswerOptionsToggleExpression, ExtItemControl
from pydantic_fhir_extensions.questionnaire import QuestionnaireItem

def test_validation_of_item_control_extension():
    json = {
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

    result = ExtItemControl.model_validate(json)

def test_validation_question_with_item_control():

    json_1 = {
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

    json_2 = {
        "itemControl":{
            "system": "http://tiro.health/fhir/CodeSystem/tiro-questionnaire-item-control",
            "code": "text-area",
            "display": "Text Area"
        },
        "type": "text",
        "text": "This is a question",
        "linkId": "question-1.1"
    }

    result = QuestionnaireItem.model_validate(json_1)
    assert result.itemControl.code == "text-area"
    assert result.itemControl.display == "Text Area"
    assert result.extension is not None and len(result.extension) == 1

    result_2 = QuestionnaireItem.model_validate(json_2)
    serialized_1 = result.model_dump_fhir()
    serialized_2 = result_2.model_dump_fhir()
    assert serialized_1 == json_1
    assert serialized_1 == serialized_2

def test_validation_of_option_toggle_expression():
    json = {
        'extension': [
            {
                'url': 'option',
                'valueCoding': {
                    'system': 'urn:CodeSystem:toggle',
                    'code': 'yes',
                    'display': 'Yes'
                }
            },
            {
                'url': 'expression',
                'valueExpression': {
                        'expression': 'count(../answer) = 0',
                        'language': 'text/fhirpath'
                    }
            }
        ],
        'url': 'http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression'
    }

    ExtAnswerOptionsToggleExpression.model_validate(json)

def test_validation_of_question_with_toggle_expression():

    json_1 = {
        "extension": [
            {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl",
                "valueCodeableConcept": {
                    "text": "Dropdown",
                    "coding": [
                        {
                            "system": "http://tiro.health/fhir/CodeSystem/tiro-questionnaire-item-control",
                            "code": "dropdown",
                            "display": "Dropdown"
                        },
                        {
                            "system": "http://hl7.org/fhir/questionnaire-item-control",
                            "code": "drop-down",
                            "display": "Drop Down"
                        }
                    ]
                }
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression",
                "extension": [
                    {
                        "url": "option",
                        "valueCoding": {
                            "system": "urn:CodeSystem:toggle",
                            "code": "yes",
                            "display": "Yes"
                        },
                    },
                    {
                        "url": "expression",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "count(../answer) = 0"
                        }
                    }
                ]
            },
            {
                "url": "http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-answerOptionsToggleExpression",
                "extension": [
                    {
                        "url": "option",
                        "valueCoding": {
                            "system": "urn:CodeSystem:toggle",
                            "code": "no",
                            "display": "No"
                        }
                    },
                    {
                        "url": "expression",
                        "valueExpression": {
                            "language": "text/fhirpath",
                            "expression": "count(../answer) > 0"
                        }
                    }
                ]
            }
        ],
        "answerOption": [
            {
                "valueCoding": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "yes",
                    "display": "Yes"
                }
            },
            {
                "valueCoding": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "no",
                    "display": "No"
                }
            }
        ],
        "type": "coding",
        "text": "This is a question",
        "linkId": "question-1.1",
    }

    json_2 = {
        "itemControl": {
            "system": "http://tiro.health/fhir/CodeSystem/tiro-questionnaire-item-control",
            "code": "dropdown",
            "display": "Dropdown"
        },
        "answerOptionsToggleExpression": [
            {
                "option": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "yes",
                    "display": "Yes"
                },
                "expression": {
                    "language": "text/fhirpath",
                    "expression": "count(../answer) = 0"
                },
            },
            {
                "option": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "no",
                    "display": "No"
                },
                "expression": {
                    "language": "text/fhirpath",
                    "expression": "count(../answer) > 0"
                },
            },
        ],
        "answerOption": [
            {
                "valueCoding": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "yes",
                    "display": "Yes"
                },
            },
            {
                "valueCoding": {
                    "system": "urn:CodeSystem:toggle",
                    "code": "no",
                    "display": "No"
                },
            },
        ],
        "type": "coding",
        "text": "This is a question",
        "linkId": "question-1.1",
    }

    result_1 = QuestionnaireItem.model_validate(json_1)
    assert len(result_1.extension) == 3
    assert result_1.answerOption is not None
    assert len(result_1.answerOption) == 2
    assert len(result_1.answerOptionsToggleExpression) == 2

    result_2 = QuestionnaireItem.model_validate(json_2)
    assert result_1.model_dump_fhir() == result_2.model_dump_fhir()
