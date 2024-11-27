import random
import numpy as np

def generateInstance(n):
    # Otwarcie pliku do zapisu w trybie 'w' (write)
    with open(f'in_151788_{n}.txt', 'w') as file:
        # Zapis liczby zadań
        file.write(f"{n}\n")
        
        # Generowanie czasów realizacji p oraz zaliczek r
        p = [random.randint(1, 50) for _ in range(n)]
        r = [random.randint(0, 100) for _ in range(n)]
        
        # Zapisanie wartości p i r dla każdego zadania
        for i in range(n):
            file.write(f"{p[i]} {r[i]}\n")
            
        # Generowanie macierzy Sij (czasy wymiany głowic)
        S = [[0 if i == j else random.randint(0, int(np.mean(p))) for j in range(n)] for i in range(n)]
        
        # Zapisanie macierzy Sij do pliku
        for row in S:
            file.write(" ".join(map(str, row)) + "\n")

# Główna funkcja
if __name__ == "__main__":
    # Rozmiary zadań: 50, 100, 150, ..., 500
    task_sizes = range(50, 501, 50)
    
    # Generowanie instancji dla każdego rozmiaru zadań
    for n in task_sizes:
        generateInstance(n)
