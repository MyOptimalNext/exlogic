import numpy as np
from typing import List, Union
from exlogic.eEncoder import float32_to_comp64
from exlogic.eDecoder import comp64_to_float32
from .eOperations import eadd, esubtract, emultiply, edivide, ereciprocal

class eTensor:
    def __init__(self,  Union[List, np.ndarray]):
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
            if isinstance(item, (int, float)):
                encoded_data.append(float32_to_comp64(float(item)))
            elif isinstance(item, np.integer) or isinstance(item, np.floating):
                encoded_data.append(float32_to_comp64(float(item)))
            else:
                encoded_data.append(item)
        
        self.data = np.array(encoded_data, dtype=object).reshape(shape)
    
    def to_numpy(self) -> np.ndarray:
        flat_data = self.data.flatten()
        decoded_data = []
        
        for item in flat_data:
            if isinstance(item, int):
                decoded_data.append(comp64_to_float32(item))
            else:
                decoded_data.append(item)
        
        return np.array(decoded_data).reshape(self.data.shape)
    
    def __str__(self) -> str:
        return str(self.to_numpy())
    
    def __repr__(self) -> str:
        return f"eTensor({self.to_numpy()})"

def etadd(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.data.shape != tensor_b.data.shape:
        raise ValueError("Tensors must have the same shape")
    
    result_data = np.empty_like(tensor_a.data, dtype=object)
    shape = tensor_a.data.shape
    
    if len(shape) == 1:
        for i in range(shape[0]):
            result_data[i] = eadd(tensor_a.data[i], tensor_b.data[i])
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                result_data[i, j] = eadd(tensor_a.data[i, j], tensor_b.data[i, j])
    else:
        flat_a = tensor_a.data.flatten()
        flat_b = tensor_b.data.flatten()
        flat_result = np.array([eadd(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
        result_data = flat_result.reshape(shape)
    
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def etsubtract(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.data.shape != tensor_b.data.shape:
        raise ValueError("Tensors must have the same shape")
    
    result_data = np.empty_like(tensor_a.data, dtype=object)
    shape = tensor_a.data.shape
    
    if len(shape) == 1:
        for i in range(shape[0]):
            result_data[i] = esubtract(tensor_a.data[i], tensor_b.data[i])
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                result_data[i, j] = esubtract(tensor_a.data[i, j], tensor_b.data[i, j])
    else:
        flat_a = tensor_a.data.flatten()
        flat_b = tensor_b.data.flatten()
        flat_result = np.array([esubtract(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
        result_data = flat_result.reshape(shape)
    
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def etmultiply(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.data.shape != tensor_b.data.shape:
        raise ValueError("Tensors must have the same shape")
    
    result_data = np.empty_like(tensor_a.data, dtype=object)
    shape = tensor_a.data.shape
    
    if len(shape) == 1:
        for i in range(shape[0]):
            result_data[i] = emultiply(tensor_a.data[i], tensor_b.data[i])
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                result_data[i, j] = emultiply(tensor_a.data[i, j], tensor_b.data[i, j])
    else:
        flat_a = tensor_a.data.flatten()
        flat_b = tensor_b.data.flatten()
        flat_result = np.array([emultiply(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
        result_data = flat_result.reshape(shape)
    
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def etdivide(tensor_a: eTensor, tensor_b: eTensor) -> eTensor:
    if tensor_a.data.shape != tensor_b.data.shape:
        raise ValueError("Tensors must have the same shape")
    
    result_data = np.empty_like(tensor_a.data, dtype=object)
    shape = tensor_a.data.shape
    
    if len(shape) == 1:
        for i in range(shape[0]):
            result_data[i] = edivide(tensor_a.data[i], tensor_b.data[i])
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                result_data[i, j] = edivide(tensor_a.data[i, j], tensor_b.data[i, j])
    else:
        flat_a = tensor_a.data.flatten()
        flat_b = tensor_b.data.flatten()
        flat_result = np.array([edivide(a, b) for a, b in zip(flat_a, flat_b)], dtype=object)
        result_data = flat_result.reshape(shape)
    
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

def etreciprocal(tensor: eTensor) -> eTensor:
    result_data = np.empty_like(tensor.data, dtype=object)
    shape = tensor.data.shape
    
    if len(shape) == 1:
        for i in range(shape[0]):
            result_data[i] = ereciprocal(tensor.data[i])
    elif len(shape) == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                result_data[i, j] = ereciprocal(tensor.data[i, j])
    else:
        flat_data = tensor.data.flatten()
        flat_result = np.array([ereciprocal(x) for x in flat_data], dtype=object)
        result_data = flat_result.reshape(shape)
    
    result = eTensor.__new__(eTensor)
    result.data = result_data
    return result

__all__ = ['eTensor', 'etadd', 'etsubtract', 'etmultiply', 'etdivide', 'etreciprocal']
