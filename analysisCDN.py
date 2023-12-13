from enum import Enum
import tldextract as tld
from resolveSOA import getSOA
import sys

class CDN_TYPE(Enum):
    UNKNOWN = 1
    PRIVATE = 2
    THIRD = 3

    