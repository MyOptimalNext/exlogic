import math

def float32_to_comp64(value: float) -> int:
    if value == 0.0:
        return 0x0000000100000001
    
    s = 1 if value >= 0 else -1
    x = math.log(abs(value))
    t = 1 if x >= 0 else -1
    abs_x = abs(x)
    i = int(abs_x)
    d = abs_x - i

    first_32 = ((0 if s == 1 else 1) << 31) | (i & 0x7FFFFFFF)
    d_scaled = int(d * 2147483647.0)
    second_32 = ((0 if t == 1 else 1) << 31) | (d_scaled & 0x7FFFFFFF)

    return (first_32 << 32) | second_32

__all__ = ['float32_to_comp64']
