from z3 import BitVec, Solver

x = BitVec('x', 64)
a = BitVec('a', 64)
b = BitVec('b', 64)
c = BitVec('c', 64)
d = BitVec('d', 64)

s = Solver()

s.add(a == x * 123)
s.add(b == a - 6)
s.add(c == b + a)
s.add(d == a + b + c)
s.add(d == 3691464)

if str(s.check()) == "sat":
    print("Answer found:", s.model()[x])
else:
    print("Could not find answer")
