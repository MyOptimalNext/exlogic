import math

def comp64_to_float32(comp_value: int) -> float:
    if comp_value == 0x0000000100000001:
        return 0.0

    first_32 = (comp_value >> 32) & 0xFFFFFFFF
    second_32 = comp_value & 0xFFFFFFFF

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
    if x > 709.0:
        return float('inf') if s == 1 else float('-inf')
    elif x < -709.0:
        return 0.0 if s == 1 else -0.0
    else:
        return s * math.exp(x)

__all__ = ['comp64_to_float32']
