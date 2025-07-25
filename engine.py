import math

class Value:

    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self._prev = set(_children)
        self.grad = 0 
        self._op = _op
        self._backward = lambda: None 
    def __repr__(self):
        return f"Value: {self.data}"

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out 

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        def _backward():
            self.grad += other.grad * out.grad
            other.grad += self.grad * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        x = self.data 
        t = (math.exp(2*x) - 1) / (math.exp(2*x) + 1)
        out = Value(t, (self, ), 'tanh')

        def _backward():
            self.grad = (1-t**2) * out.grad
        out._backward = _backward

        return out 
    

    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(v)
                topo.append(v)
        build_topo(self)

        self.grad = 1

        for v in reversed(topo):
            v._backward()


    def __rmul__(self, other):
        return self * other
    
    def exp(self):
        x = self.data 
        out = Value(math.exp(self.data), (self, ), 'exp')

        def _backward():
            self.grad = out.data*out.grad 

        self._backward = _backward

        return out 
    
    


