from pydantic import BaseModel
from enum import Enum
from typing import List


class AlgorithmType(str, Enum):
    SHANNON = "shannon_entropy"
    APPROXIMATE = "approximate_entropy"
    SAMPLE = "sample_entropy"
    PERMUTATION = "permutation_entropy"
    MULTISCALE = "multiscale_entropy"


class EntropyResult(BaseModel):
    encoding: str
    algorithm: str
    entropy: float


class EntropyResponse(BaseModel):
    results: List[EntropyResult]


class EncodingModel(Enum):
    """Supported encoding models."""

    ORDINAL = "ordinal"
    ONE_HOT = "one_hot"
    FREQUENCY = "frequency"
    BINARY = "binary"
