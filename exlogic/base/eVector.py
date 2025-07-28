import numpy as np
from typing import List, Union
from exlogic.eEncoder import float32_to_comp64
from exlogic.eDecoder import comp64_to_float32
from exlogic.base.eOperations import eadd, esubtract, emultiply, edivide, ereciprocal

class eVector:
    def __init__(self, data: Union[List, np.ndarray]):
        if isinstance(data, list):
            self.data = np.array(data, dtype=object)
            self._encode_data()
        elif isinstance(data, np.ndarray):
            self.data = data.astype(object)
            self._encode_data()
        else:
            raise TypeError("Data must be list or numpy array")

    def _encode_data(self):
        encoded = []
        for item in self.data:
            if isinstance(item, (int, float, np.integer, np.floating)):
                encoded.append(float32_to_comp64(float(item)))
            else:
                encoded.append(item)
        self.data = np.array(encoded, dtype=object)

    def to_numpy(self) -> np.ndarray:
        decoded = []
        for item in self.data:
            if isinstance(item, (int, float, np.integer, np.floating)):
                decoded.append(comp64_to_float32(int(item)))
            else:
                decoded.append(item)
        return np.array(decoded)

    @property
    def shape(self) -> tuple:
        return self.data.shape

    def __str__(self) -> str:
        return str(self.to_numpy())

    def __repr__(self) -> str:
        return f"eVector({self.to_numpy()})"

def elem_add(vec_a: eVector, vec_b: eVector) -> eVector:
    if vec_a.shape != vec_b.shape:
        raise ValueError("Vectors must have the same shape")
    result_encoded = [eadd(a, b) for a, b in zip(vec_a.data, vec_b.data)]
    result = eVector.__new__(eVector)
    result.data = np.array(result_encoded, dtype=object)
    return result

def elem_subtract(vec_a: eVector, vec_b: eVector) -> eVector:
    if vec_a.shape != vec_b.shape:
        raise ValueError("Vectors must have the same shape")
    result_encoded = [esubtract(a, b) for a, b in zip(vec_a.data, vec_b.data)]
    result = eVector.__new__(eVector)
    result.data = np.array(result_encoded, dtype=object)
    return result

def elem_multiply(vec_a: eVector, vec_b: eVector) -> eVector:
    if vec_a.shape != vec_b.shape:
        raise ValueError("Vectors must have the same shape")
    result_encoded = [emultiply(a, b) for a, b in zip(vec_a.data, vec_b.data)]
    result = eVector.__new__(eVector)
    result.data = np.array(result_encoded, dtype=object)
    return result

def elem_divide(vec_a: eVector, vec_b: eVector) -> eVector:
    if vec_a.shape != vec_b.shape:
        raise ValueError("Vectors must have the same shape")
    result_encoded = [edivide(a, b) for a, b in zip(vec_a.data, vec_b.data)]
    result = eVector.__new__(eVector)
    result.data = np.array(result_encoded, dtype=object)
    return result

def elem_reciprocal(vec: eVector) -> eVector:
    result_encoded = [ereciprocal(x) for x in vec.data]
    result = eVector.__new__(eVector)
    result.data = np.array(result_encoded, dtype=object)
    return result

def dot_product(vec_a: eVector, vec_b: eVector) -> int:
    if vec_a.shape != vec_b.shape:
        raise ValueError("Vectors must have the same shape")
    result = float32_to_comp64(0.0)
    for a, b in zip(vec_a.data, vec_b.data):
        product = emultiply(a, b)
        result = eadd(result, product)
    return result
