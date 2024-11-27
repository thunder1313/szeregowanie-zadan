import sys
import time
import heapq

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        
        p = [int(lines[i+1].split()[0]) for i in range(n)]
        r = [int(lines[i+1].split()[1]) for i in range(n)]
        
        S = [list(map(int, lines[i + n + 1].split())) for i in range (n)]

    return n, p, r, S

def write_output(filename, best_F, sequence):
    with open(filename, 'w') as file:
        file.write(f"{best_F}\n")
        file.write(" ".join(map(str, [task for task in sequence])) + "\n")


def evaluate_permutation(sequence, p, r, S):
    current_time = 0
    total_flow_time = 0
    previous_task = 0

    for task in sequence:
        task_index = task - 1

        if previous_task != 0:
            current_time += S[previous_task - 1][task_index]

        start_time = max(current_time, r[task_index])

        completion_time = start_time + p[task_index]
        flow_time = completion_time - r[task_index]
        total_flow_time += flow_time

        current_time = completion_time
        previous_task = task

    return total_flow_time

def find_solution(n, p, r, S, time_limit):
    start_time = time.time()
    current_time = 0
    previous_task = None
    sequence = []
    remaining_tasks = set(range(1, n + 1))

    while remaining_tasks:
        best_task = min(
            remaining_tasks,
            key=lambda task: max(current_time + (S[previous_task - 1][task - 1] if previous_task else 0), r[task - 1])
        )

        task_index = best_task - 1
        setup_time = S[previous_task - 1][task_index] if previous_task else 0
        best_time = max(current_time + setup_time, r[task_index])
        
        sequence.append(best_task)
        remaining_tasks.remove(best_task)
        current_time = best_time + p[task_index]
        previous_task = best_task

    return evaluate_permutation(sequence, p, r, S), sequence


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python 151788.py <input_file> <output_file> <time_limit>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])
    n, p, r, S = read_instance(input_file)
    best_F, sequence = find_solution(n, p, r, S, time_limit)
    write_output(output_file, best_F, sequence)