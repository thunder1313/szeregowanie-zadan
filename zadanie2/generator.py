import random
import numpy as np

def generateInstance(n):
    with open(f'in_151788_{n}.txt', 'w') as file:
        file.write(f"{n}\n")
        
        p1 = [random.randint(1, 50) for _ in range(n)]
        p2 = [random.randint(1, 50) for _ in range(n)]
        p3 = [random.randint(1, 50) for _ in range(n)]
        p4 = [random.randint(1, 50) for _ in range(n)]
        w = [random.randint(1, 10) for _ in range(n)]
        d = [random.randint(50, 200) for _ in range(n)]
        
        for i in range(n):
            file.write(f"{p1[i]} {p2[i]} {p3[i]} {p4[i]} {w[i]} {d[i]}\n")

if __name__ == "__main__":
    task_sizes = range(50, 501, 50)
    for n in task_sizes:
        generateInstance(n)