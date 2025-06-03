import re
from typing import ClassVar, Self


class _RegexStr(str):
    """Generic “string with regex validation” base class."""

    _PATTERN: ClassVar[re.Pattern[str]]

    # Pydantic hook
    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, v: str) -> Self:
        if not isinstance(v, str):
            raise TypeError("value must be a string")
        if not cls._PATTERN.fullmatch(v):
            raise ValueError(f"invalid {cls.__name__} format: {v!r}")
        return cls(v)

    # nicer repr in logs / notebooks
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{str(self)}')"


class Cid(_RegexStr):
    """Identifiant commun (16 chars)."""

    _PATTERN = re.compile(r"^[A-Z]{3}[A-Z0-9]{13}$")


class Eli(_RegexStr):
    """European Legislation Identifier."""

    _PATTERN = re.compile(r"^eli/[a-zA-Z0-9_\-/:.]+$")


class Nor(_RegexStr):
    """Numéro d'Ordre Réglementaire (NOR)."""

    _PATTERN = re.compile(r"^[A-Z]{4}[0-9]{2}[0-9]{5}[A-Z]$")
