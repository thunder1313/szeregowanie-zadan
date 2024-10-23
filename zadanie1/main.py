import itertools
import sys
import time

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        
        p = [int(lines[i + 1].split()[0]) for i in range(n)]
        r = [int(lines[i + 1].split()[1]) for i in range(n)]
        
        S = [list(map(int, lines[i + n + 1].split())) for i in range(n)]

    return n, p, r, S

def write_output(filename, F, schedule):
    with open(filename, 'w') as file:
        file.write(f"{F}\n")
        file.write(" ".join(map(str, [task for task in schedule])) + "\n")

def evaluate_schedule(sequence, p, r, S):
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

def schedule_heuristic(n, p, r, S):
    # Unvisited tasks
    unvisited = set(range(1, n+1))
    
    # Start with the task that has the earliest release time
    current_time = 0
    current_task = min(unvisited, key=lambda i: r[i])
    schedule = [current_task]
    unvisited.remove(current_task)
    current_time = max(r[current_task], current_time) + p[current_task]
    
    while unvisited:
        # Find tasks that are available (released)
        available_tasks = [task for task in unvisited if r[task] <= current_time]
        
        if available_tasks:
            # From the available tasks, choose the one with the shortest setup time from current_task
            next_task = min(available_tasks, key=lambda i: S[current_task][i])
        else:
            # If no task is available, wait until the next task is released
            next_task = min(unvisited, key=lambda i: r[i])
            current_time = r[next_task]
        
        # Schedule the next task and update the current time
        schedule.append(next_task)
        unvisited.remove(next_task)
        current_time = max(r[next_task], current_time + S[current_task][next_task]) + p[next_task]
        current_task = next_task
        
    F = evaluate_schedule(schedule, p, r, S)
    
    return F, schedule

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <input_file> <output_file> <time_limit>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])
    print(input_file)
    n, p, r, S = read_instance(input_file)
    best_F, schedule = schedule_heuristic(n, p, r, S, time_limit)
    write_output(output_file, best_F, schedule)