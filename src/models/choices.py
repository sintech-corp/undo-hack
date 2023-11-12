import enum
from typing import Literal


class GenderChoices(str, enum.Enum):
    MALE = "m"
    FEMALE = "f"


class CommunicationRequestStatuses(str, enum.Enum):
    OPEN = "open"
    IN_PROCESS = "in_process"
    CLOSED = "closed"


LanguageCodes = Literal["ru", "ro", "en"]
