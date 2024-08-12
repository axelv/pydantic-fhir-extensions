from typing import Protocol

from pydantic_fhir_extensions.types.coding import Coding


class CodeableConcept(Protocol):
    @property
    def text(self) -> str:
        ...

    @property
    def coding(self) -> list[Coding]:
        ...
