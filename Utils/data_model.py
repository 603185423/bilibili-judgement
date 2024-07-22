from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class InstanceOperation(Enum):
    NONE = 'status'
    STATUS = 'status'
    ON = 'on'
    OFF = 'off'
    REBOOT = 'reboot'
    HARD_OFF = 'hard_off'
    HARD_REBOOT = 'hard_reboot'


@dataclass
class TranslationText:
    original_text: str = ''
    translated_text: str = ''
