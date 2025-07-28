import random from typing import Any, List, Tuple from exlogic.eEncoder import float32_to_comp64

Tensor = List[List[int]]

ENCODED_ZERO = float32_to_comp64(0.0)

def etensor_empty(shape: Tuple[int, int]) -> Tensor: rows, cols = shape return [[ENCODED_ZERO for _ in range(cols)] for _ in range(rows)]

def etensor_full(shape: Tuple[int, int], value: float) -> Tensor: comp64_val = float32_to_comp64(value) rows, cols = shape return [[comp64_val for _ in range(cols)] for _ in range(rows)]

def etensor_zeros(shape: Tuple[int, int]) -> Tensor: return etensor_full(shape, 0.0)

def etensor_ones(shape: Tuple[int, int]) -> Tensor: return etensor_full(shape, 1.0)

def etensor_identity(size: int) -> Tensor: tensor = etensor_zeros((size, size)) for i in range(size): tensor[i][i] = float32_to_comp64(1.0) return tensor

def etensor_eye(rows: int, cols: int, k: int = 0) -> Tensor: tensor = etensor_zeros((rows, cols)) for i in range(rows): j = i + k if 0 <= j < cols: tensor[i][j] = float32_to_comp64(1.0) return tensor

def etensor_random(shape: Tuple[int, int], min_val: float = 0.0, max_val: float = 1.0) -> Tensor: rows, cols = shape return [[float32_to_comp64(random.uniform(min_val, max_val)) for _ in range(cols)] for _ in range(rows)]

def etensor_shape(tensor: Tensor) -> Tuple[int, int]: return len(tensor), len(tensor[0]) if tensor else 0

def etensor_transpose(tensor: Tensor) -> Tensor: rows, cols = etensor_shape(tensor) return [[tensor[i][j] for i in range(rows)] for j in range(cols)]

def etensor_flip(tensor: Tensor, axis: int = 0) -> Tensor: if axis == 0: return tensor[::-1] if axis == 1: return [row[::-1] for row in tensor] raise ValueError("Axis must be 0 or 1")

def etensor_reverse(tensor: Tensor) -> Tensor: return etensor_flip(etensor_flip(tensor, axis=0), axis=1)

def etensor_reshape(tensor: Tensor, new_shape: Tuple[int, int]) -> Tensor: rows, cols = etensor_shape(tensor) total = rows * cols new_rows, new_cols = new_shape if new_rows * new_cols != total: raise ValueError(f"Cannot reshape array of size {total} into shape {new_shape}") flat = [tensor[i][j] for i in range(rows) for j in range(cols)] return [flat[i*new_cols:(i+1)*new_cols] for i in range(new_rows)]

def etensor_flatten(tensor: Tensor) -> List[int]: rows, cols = etensor_shape(tensor) return [tensor[i][j] for i in range(rows) for j in range(cols)]

all = [ 'etensor_empty', 'etensor_full', 'etensor_zeros', 'etensor_ones', 'etensor_identity', 'etensor_eye', 'etensor_random', 'etensor_shape', 'etensor_transpose', 'etensor_flip', 'etensor_reverse', 'etensor_reshape', 'etensor_flatten' ]

