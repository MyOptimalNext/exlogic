import math
from ..eEncoder import float32_to_comp64
from ..eDecoder import comp64_to_float32

def eadd(comp64_a: int, comp64_b: int) -> int:
    a = comp64_to_float32(comp64_a)
    b = comp64_to_float32(comp64_b)
    result = a + b
    return float32_to_comp64(result)

def emultiply(comp64_a: int, comp64_b: int) -> int:
    if comp64_a == 0x0000000100000001 or comp64_b == 0x0000000100000001:
        return 0x0000000100000001
    
    first_32_a = (comp64_a >> 32) & 0xFFFFFFFF
    second_32_a = comp64_a & 0xFFFFFFFF
    s_a = 0 if (first_32_a >> 31) & 1 == 0 else 1
    t_a = 0 if (second_32_a >> 31) & 1 == 0 else 1
    i_a = first_32_a & 0x7FFFFFFF
    if i_a >= 0x40000000:
        i_a = i_a - 0x80000000
    d_scaled_a = second_32_a & 0x7FFFFFFF
    d_a = d_scaled_a / 2147483647.0
    log_a = (1 if t_a == 0 else -1) * (i_a + d_a)
    
    first_32_b = (comp64_b >> 32) & 0xFFFFFFFF
    second_32_b = comp64_b & 0xFFFFFFFF
    s_b = 0 if (first_32_b >> 31) & 1 == 0 else 1
    t_b = 0 if (second_32_b >> 31) & 1 == 0 else 1
    i_b = first_32_b & 0x7FFFFFFF
    if i_b >= 0x40000000:
        i_b = i_b - 0x80000000
    d_scaled_b = second_32_b & 0x7FFFFFFF
    d_b = d_scaled_b / 2147483647.0
    log_b = (1 if t_b == 0 else -1) * (i_b + d_b)
    
    log_result = log_a + log_b
    s_result = s_a ^ s_b
    
    if log_result > 709.0:
        return 0x7FF0000000000000 if s_result == 0 else 0xFFF0000000000000
    elif log_result < -709.0:
        return 0x0000000100000001
    
    value_result = math.exp(abs(log_result))
    if s_result == 1:
        value_result = -value_result
    return float32_to_comp64(value_result)

def epower(comp64_base: int, comp64_exponent: int) -> int:
    base = comp64_to_float32(comp64_base)
    exponent = comp64_to_float32(comp64_exponent)
    
    if base == 0.0 and exponent > 0:
        return 0x0000000100000001
    elif base == 1.0:
        return float32_to_comp64(1.0)
    elif exponent == 0.0:
        return float32_to_comp64(1.0)
    
    try:
        result = pow(base, exponent)
        return float32_to_comp64(result)
    except:
        return float32_to_comp64(float('inf'))

__all__ = ['eadd', 'emultiply', 'epower']
