from z3 import BitVec, Solver

x = BitVec('x', 64)
a = BitVec('a', 64)
b = BitVec('b', 64)
c = BitVec('c', 64)
d = BitVec('d', 64)

# Instiantiate the solver engine
s = Solver()

# Add constraints
# Example: s.add(a == x * 123)


# Run solver and print result
if str(s.check()) == "sat":
    print(s.model()[x])
else:
    print("Could not find the answer using the given constraints")
