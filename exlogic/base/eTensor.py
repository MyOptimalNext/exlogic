import numpy as np
from typing import List, Union
from exlogic.eEncoder import float32_to_comp64
from exlogic.eDecoder import comp64_to_float32
from exlogic.base.eOperations import eadd, esubtract, emultiply, edivide, ereciprocal

class eTensor:
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
        shape = self.data.shape
        flat_data = self.data.flatten()
        encoded_data = []
        for item in flat_data:
            if isinstance(item, (int, float, np.integer, np.floating)):
                encoded_data.append(float32_to_comp64(float(item)))
            else:
                encoded_data.append(item)
        self.data = np.array(encoded_data, dtype=object).reshape(shape)

    def to_numpy(self) -> np.ndarray:
        shape = self.data.shape
        flat_data = self.data.flatten()
        decoded_data = []
        for item in flat_data:
            if isinstance(item, (int, float, np.integer, np.floating)):
                decoded_data.append(comp64_to_float32(int(item)))
            else:
                decoded_data.append(item)
        return np.array(decoded_data).reshape(shape)

    @property
    def shape(self) -> tuple:
        return self.data.shape

    def __str__(self) -> str:
        return str(self.to_numpy())

    def __repr__(self) -> str:
        return f"eTensor({self.to_numpy()})"

def elem_add(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.shape != tensor_b.shape:
        raise ValueError("Tensors must have the same shape")
    flat_a = tensor_a.data.flatten()
    flat_b = tensor_b.data.flatten()
    flat_result = np.array([eadd(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
    result_data = flat_result.reshape(tensor_a.shape)
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def elem_subtract(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.shape != tensor_b.shape:
        raise ValueError("Tensors must have the same shape")
    flat_a = tensor_a.data.flatten()
    flat_b = tensor_b.data.flatten()
    flat_result = np.array([esubtract(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
    result_data = flat_result.reshape(tensor_a.shape)
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def elem_multiply(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.shape != tensor_b.shape:
        raise ValueError("Tensors must have the same shape")
    flat_a = tensor_a.data.flatten()
    flat_b = tensor_b.data.flatten()
    flat_result = np.array([emultiply(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
    result_data = flat_result.reshape(tensor_a.shape)
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def elem_divide(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.shape != tensor_b.shape:
        raise ValueError("Tensors must have the same shape")
    flat_a = tensor_a.data.flatten()
    flat_b = tensor_b.data.flatten()
    flat_result = np.array([edivide(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
    result_data = flat_result.reshape(tensor_a.shape)
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def elem_reciprocal(tensor: eTensor) -> eTensor:
    flat_data = tensor.data.flatten()
    flat_result = np.array([ereciprocal(x) for x in flat_data], dtype=object)
    result_data = flat_result.reshape(tensor.shape)
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def matrix_multiply(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if len(tensor_a.shape) != 2 or len(tensor_b.shape) != 2:
        raise ValueError("Matrix multiplication requires 2D tensors")
    if tensor_a.shape[1] != tensor_b.shape[0]:
        raise ValueError("Matrix dimensions incompatible for multiplication")

    rows_a, cols_a = tensor_a.shape
    _, cols_b = tensor_b.shape
    result_data = np.empty((rows_a, cols_b), dtype=object)

    for i in range(rows_a):
        for j in range(cols_b):
            sum_element = float32_to_comp64(0.0)
            for k in range(cols_a):
                product = emultiply(tensor_a.data[i, k], tensor_b.data[k, j])
                sum_element = eadd(sum_element, product)
            result_data[i, j] = sum_element

    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def transpose(tensor: eTensor) -> eTensor:
    if len(tensor.shape) != 2:
        raise ValueError("Transpose requires 2D tensor")
    result_data = tensor.data.T.copy()
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result
