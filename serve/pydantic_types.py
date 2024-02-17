from pydantic import BaseModel
from typing import Dict


class InputIris(BaseModel):
    petal_length: float
    petal_width: float


class OutputPredict(BaseModel):
    results: Dict[str, float]