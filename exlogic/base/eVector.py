from typing import List
from exlogic.eEncoder import float32_to_comp64
import random

Vector = List[int]

ENCODED_ZERO = float32_to_comp64(0.0)

def evector_empty(length: int) -> Vector:
    return [ENCODED_ZERO for _ in range(length)]

def evector_full(length: int, value: float) -> Vector:
    comp64_val = float32_to_comp64(value)
    return [comp64_val for _ in range(length)]

def evector_zeros(length: int) -> Vector:
    return evector_full(length, 0.0)

def evector_ones(length: int) -> Vector:
    return evector_full(length, 1.0)

def evector_random(length: int, min_val: float = 0.0, max_val: float = 1.0) -> Vector:
    return [float32_to_comp64(random.uniform(min_val, max_val)) for _ in range(length)]

def evector_flatten(vector: Vector) -> List[int]:
    return vector[:]

def evector_length(vector: Vector) -> int:
    return len(vector)

def evector_reverse(vector: Vector) -> Vector:
    return vector[::-1]

__all__ = [
    'evector_empty', 'evector_full', 'evector_zeros', 'evector_ones',
    'evector_random', 'evector_flatten', 'evector_length', 'evector_reverse'
]
