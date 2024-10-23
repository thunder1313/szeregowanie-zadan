import subprocess
import time
import sys

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        
        p = [int(lines[i + 1].split()[0]) for i in range(n)]
        r = [int(lines[i + 1].split()[1]) for i in range(n)]
        
        S = [list(map(int, lines[i + n + 1].split())) for i in range(n)]

    return n, p, r, S



def read_solution(filename):
    with open(filename, 'r') as file:
        F = int(file.readline().strip())
        sequence = list(map(int, file.readline().split()))
    return F, sequence

def run_time_verification(executable, input_file, output_file, time_limit):
    start_time = time.time()
    
    try:
        print(f"Running: {executable} {input_file} {output_file} {time_limit}")

        result = subprocess.run(
            [executable, input_file, output_file, str(time_limit)],
            timeout=time_limit,
            capture_output=True,
            text=True
        )
        end_time = time.time()
        elapsed_time = end_time - start_time

        if result.returncode != 0:
            print(f"Program terminated with an error. Return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            print(f"Standard output: {result.stdout}")
        else:
            print(f"Program executed successfully.")
            print(f"Output: {result.stdout}")

        print(f"Elapsed time: {elapsed_time:.2f} seconds")

    except subprocess.TimeoutExpired:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Program exceeded the time limit of {time_limit} seconds.")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")


def validate_solution(num_tasks, processing_times, release_times, setup_times, expected_flow_time, task_sequence):
    errors = []
    expected_tasks = set(range(1, num_tasks + 1))

    # Check if the sequence contains all tasks exactly once
    if len(task_sequence) != num_tasks or set(task_sequence) != expected_tasks:
        errors.append("Not all tasks are present exactly once in the solution.")

    current_time = 0
    total_flow_time = 0
    last_task = None

    for task in task_sequence:
        task_index = task - 1

        # Add setup time if not the first task
        if last_task is not None:
            current_time += setup_times[last_task - 1][task_index]

        # Determine the start time for the current task
        start_time = max(current_time, release_times[task_index])

        # Check if the task starts before its release time
        if start_time < release_times[task_index]:
            errors.append(f"Task {task} starts before its release time.")

        # Calculate completion time and flow time
        completion_time = start_time + processing_times[task_index]
        flow_time = completion_time - release_times[task_index]
        total_flow_time += flow_time

        # Update the current time and last task
        current_time = completion_time
        last_task = task

    # Validate the total flow time against the expected value
    if total_flow_time != expected_flow_time:
        errors.append(f"Calculated flow time ({total_flow_time}) does not match the expected value ({expected_flow_time}).")

    return errors, total_flow_time

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python weryfikator_czasu.py <executable> <input_file> <output_file> <time_limit>")
        sys.exit(1)

    executable = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    time_limit = int(sys.argv[4])
    
    n, p, r, S = read_instance(input_file)
    F, sequence = read_solution(output_file)

    errors, calculated_F = validate_solution(n, p, r, S, F, sequence)

    print(f"Given value: {F}")
    print(f"Calculated value: {calculated_F}")
    if errors:
        for error in errors:
            print(error)

    run_time_verification(executable, input_file, output_file, time_limit)