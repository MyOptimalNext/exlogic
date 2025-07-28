from exlogic.eEncoder import float32_to_comp64 from exlogic.eDecoder import comp64_to_float32 from exlogic.eArithmetic import eadd, esubtract, emultiply, edivide, ereciprocal import random

class eTensor: def init(self, values): self.values = self._encode_tensor(values)

def _encode_tensor(self, values):
    if isinstance(values[0], list):
        return [[float32_to_comp64(v) for v in row] for row in values]
    return [float32_to_comp64(v) for v in values]

def shape(self):
    if isinstance(self.values[0], list):
        return (len(self.values), len(self.values[0]))
    return (len(self.values),)

def matmul(self, other):
    a, b = self.values, other.values
    m, n = len(a), len(a[0])
    n2, p = len(b), len(b[0])
    assert n == n2, "incompatible shapes"
    result = []
    for i in range(m):
        row = []
        for j in range(p):
            sum_elem = emultiply(a[i][0], b[0][j])
            for k in range(1, n):
                sum_elem = eadd(sum_elem, emultiply(a[i][k], b[k][j]))
            row.append(sum_elem)
        result.append(row)
    return eTensor(result)

def transpose(self):
    values = self.values
    if isinstance(values[0], list):
        return eTensor([[values[j][i] for j in range(len(values))] for i in range(len(values[0]))])
    return eTensor([[v] for v in values])

def reshape(self, new_shape):
    flat = self.flatten().values
    assert new_shape[0] * new_shape[1] == len(flat)
    reshaped = []
    for i in range(new_shape[0]):
        row = []
        for j in range(new_shape[1]):
            row.append(flat[i * new_shape[1] + j])
        reshaped.append(row)
    return eTensor(reshaped)

def flatten(self):
    if isinstance(self.values[0], list):
        return eTensor([v for row in self.values for v in row])
    return self

def softmax(self):
    exp_rows = []
    for row in self.values:
        decoded = [comp64_to_float32(v) for v in row]
        max_val = max(decoded)
        exp_vals = [math.exp(v - max_val) for v in decoded]
        sum_exp = sum(exp_vals)
        normalized = [float32_to_comp64(v / sum_exp) for v in exp_vals]
        exp_rows.append(normalized)
    return eTensor(exp_rows)

def __repr__(self):
    return f"eTensor({self.values})"

@staticmethod
def zeros(shape):
    if len(shape) == 1:
        return eTensor([0.0] * shape[0])
    return eTensor([[0.0] * shape[1] for _ in range(shape[0])])

@staticmethod
def ones(shape):
    if len(shape) == 1:
        return eTensor([1.0] * shape[0])
    return eTensor([[1.0] * shape[1] for _ in range(shape[0])])

@staticmethod
def full(shape, fill_value):
    val = float32_to_comp64(fill_value)
    if len(shape) == 1:
        return eTensor([fill_value] * shape[0])
    return eTensor([[fill_value] * shape[1] for _ in range(shape[0])])

@staticmethod
def random(shape):
    if len(shape) == 1:
        return eTensor([random.random() for _ in range(shape[0])])
    return eTensor([[random.random() for _ in range(shape[1])] for _ in range(shape[0])])

all = ['eTensor']

