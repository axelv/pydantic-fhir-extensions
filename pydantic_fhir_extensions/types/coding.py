from typing import Protocol


class Coding(Protocol)
    @property
    def system(self)->str|None:
        ...

    @property
    def code(self)->str:
        ...

    @property
    def display(self)->str|None:
        ...

    @property
    def userSelected(self)->bool|None:
        ...

    @property
    def version(self)->str|None:
        ...
