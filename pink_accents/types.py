import re

from typing import Dict, Union, Callable, Optional, Sequence

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

ReplacementDictType = Dict[
    Union[ReplacedType],
    Union[int, float, DynamicWeightFnType],
]

ReplacementType = Union[
    str,
    ReplacementCallableType,
    ReplacementSequenceType,
    ReplacementDictType,
]

PatternMapType = Dict[
    Union[re.Pattern[str], str],
    ReplacementType,
]
