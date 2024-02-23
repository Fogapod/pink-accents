import re

from collections.abc import Callable, Sequence
from typing import Optional, Union

from .match import Match

DynamicWeightFnType = Callable[[int], float]

ReplacedType = Optional[str]

ReplacementCallableType = Callable[[Match], ReplacedType]

ReplacementSequenceType = Sequence[
    Union[
        ReplacedType,
        ReplacementCallableType,
    ]
]

ReplacementDictType = dict[
    Union[ReplacedType],
    Union[int, float, DynamicWeightFnType],
]

ReplacementType = Union[
    str,
    ReplacementCallableType,
    ReplacementSequenceType,
    ReplacementDictType,
]

PatternMapType = dict[
    Union[re.Pattern[str], str],
    ReplacementType,
]
