import os

for i in range(10000):
    print(i)
    result = os.popen(f"./pin {i}").read()
    if not "Incorrect" in result:
        print(f"Pin found: {i}")
        break
