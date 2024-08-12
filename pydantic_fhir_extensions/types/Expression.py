
from typing import Protocol


class InlineExpression(Protocol):

    @property
    def description(self)->str|None:
        ...

    @property
    def name(self)->str|None:
        ...

    @property
    def language(self)->str:
        ...

    @property
    def expression(self)->str:
        ...

class LibraryExpression(Protocol):

    @property
    def description(self)->str|None:
        ...

    @property
    def name(self)->str|None:
        ...

    @property
    def language(self)->str:
        ...

    @property
    def reference(self)->str:
        ...

Expression = InlineExpression | LibraryExpression
