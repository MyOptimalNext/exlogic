import math
from ..eEncoder import float32_to_comp64
from ..eDecoder import comp64_to_float32

def eadd(comp64_a: int, comp64_b: int) -> int:
    a = comp64_to_float32(comp64_a)
    b = comp64_to_float32(comp64_b)
    result = a + b
    return float32_to_comp64(result)

def esubtract(comp64_a: int, comp64_b: int) -> int:
    a = comp64_to_float32(comp64_a)
    b = comp64_to_float32(comp64_b)
    result = a - b
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

def edivide(comp64_a: int, comp64_b: int) -> int:
    if comp64_b == 0x0000000100000001:
        raise ZeroDivisionError("math error")
    
    if comp64_a == 0x0000000100000001:
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
    
    log_result = log_a - log_b
    s_result = s_a ^ s_b
    
    if log_result > 709.0:
        return 0x7FF0000000000000 if s_result == 0 else 0xFFF0000000000000
    elif log_result < -709.0:
        return 0x0000000100000001
    
    value_result = math.exp(abs(log_result))
    if s_result == 1:
        value_result = -value_result
    return float32_to_comp64(value_result)

def ereciprocal(comp64_a: int) -> int:
    if comp64_a == 0x0000000100000001:
        raise ZeroDivisionError("math error")
    
    first_32 = (comp64_a >> 32) & 0xFFFFFFFF
    second_32 = comp64_a & 0xFFFFFFFF
    
    s_bit = (first_32 >> 31) & 1
    s = 1 if s_bit == 0 else -1
    i = first_32 & 0x7FFFFFFF
    if i >= 0x40000000:
        i = i - 0x80000000
    
    t_bit = (second_32 >> 31) & 1
    t = 1 if t_bit == 0 else -1
    d_scaled = second_32 & 0x7FFFFFFF
    d = d_scaled / 2147483647.0
    
    x = t * (i + d)
    
    reciprocal_log = -x
    
    if reciprocal_log > 709.0:
        return 0x7FF0000000000000 if s == 1 else 0xFFF0000000000000
    elif reciprocal_log < -709.0:
        return 0x0000000100000001
    else:
        value_result = s * math.exp(abs(reciprocal_log))
        if s == -1 and reciprocal_log < 0:
            value_result = -value_result
        return float32_to_comp64(value_result)

__all__ = ['eadd', 'esubtract', 'emultiply', 'edivide', 'ereciprocal']
