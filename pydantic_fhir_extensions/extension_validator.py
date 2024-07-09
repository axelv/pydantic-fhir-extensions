from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Generic, Iterable, Literal, Protocol, Self, Sequence, Type, TypeVar, TypedDict

from pydantic import BaseModel, GetCoreSchemaHandler, SerializationInfo, SerializerFunctionWrapHandler, TypeAdapter, ValidationError, ValidationInfo, WrapSerializer
from pydantic.fields import FieldInfo
from pydantic.main import IncEx
from pydantic_core import CoreSchema, PydanticOmit, core_schema

from pydantic_fhir_extensions.util import is_serialization_to_fhir

TUrl = TypeVar('TUrl', bound=str)
TPropertyValue = TypeVar('TPropertyValue')

class Extension(Protocol, Generic[TUrl]):

    url: TUrl

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
    ) -> Self:
        ...

    def model_dump(
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx = None,
        exclude: IncEx = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal['none', 'warn', 'error'] = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        ...

    model_fields: ClassVar[dict[str, FieldInfo]]

class PropertyExtension(Extension[TUrl], Protocol, Generic[TUrl, TPropertyValue]):

    @classmethod
    def to_property_value(cls, *extension:Self)->TPropertyValue:
       ...

    @classmethod
    def from_property_value(cls, value:TPropertyValue, /)->Iterable[Self]:
        ...

def type_is_sequence(type_:Type)->bool:
    return type_.__name__ in ("List", "Sequence", "Tuple")

def is_empty(value:Any|None, multiple:bool)->bool:
    if multiple:
        return value is None or len(value) == 0
    return value is None

def create_default_factory(multiple:bool = False)->Callable[[],Any]:
    return list if multiple else lambda: None

@dataclass()
class ExtensionValidator:
    extension_model: Type[PropertyExtension]
    url: str = field(init=False)

    def __post_init__(self):
        # Check the 'url' field and extract the default value
        assert "url" in self.extension_model.model_fields, "Extension model must have a 'url' field"
        self.url = self.extension_model.model_fields["url"].default
        assert self.url is not None, "Extension model must have a default value for 'url' field"

    def match(self, ext:Extension)->bool:
        return ext.url == self.url

    def __get_pydantic_core_schema__(
            self, source_type: Any, handler: GetCoreSchemaHandler
        ) -> CoreSchema:
            adapter = TypeAdapter(source_type)
            multiple = type_is_sequence(source_type)

            def validator(v, info:ValidationInfo):
                """Find matching extension and validate the value"""
                if not is_empty(v, multiple):
                    return v
                prop_generator = self.extract_property(info.data.get("extension",[]))
                prop_value = next(prop_generator) if not multiple else list(prop_generator)
                return adapter.validate_python(prop_value)

            schema = core_schema.with_default_schema(
                core_schema.with_info_before_validator_function(
                    validator,
                    handler(source_type),
                ),
                default_factory=create_default_factory(multiple),
                validate_default=True,
                strict=False
            )
            return schema

    def extract_property(self, extensions:Iterable[Extension]):
        for ext in filter(self.match, extensions):
            ext_valid = self.extension_model.model_validate(ext.model_dump(exclude_unset=True))
            yield ext_valid.to_property_value()
