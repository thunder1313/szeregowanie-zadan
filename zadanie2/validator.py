import sys

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        p = []
        w = []
        d = []

        for line in lines[1:]:
            values = list(map(int, line.split()))
            p.append(values[:4])  # Processing times for 4 machines
            w.append(values[4])  # Penalty weight
            d.append(values[5])  # Deadline

    return n, p, w, d

def read_solution(filename):
    with open(filename, 'r') as file:
        total_penalty = int(file.readline().strip())
        schedule = [list(map(int, line.split())) for line in file]
    return total_penalty, schedule

def validate_solution(num_jobs, processing_times, weights, deadlines, expected_penalty, machine_schedule):
    errors = []
    job_completion_times = [0] * num_jobs
    job_assigned = [False] * num_jobs
    total_penalty = 0

    # Validate job assignments and calculate completion times
    for machine_id, machine_jobs in enumerate(machine_schedule):
        current_time = 0
        for job in machine_jobs:
            if job < 1 or job > num_jobs:
                errors.append(f"Invalid job number {job} on machine {machine_id + 1}.")
                continue

            job_index = job - 1
            if job_assigned[job_index]:
                errors.append(f"Job {job} is assigned to multiple machines.")
                continue

            job_assigned[job_index] = True
            current_time += processing_times[job_index][machine_id]
            job_completion_times[job_index] = current_time

    # Check for unassigned jobs
    for i, assigned in enumerate(job_assigned):
        if not assigned:
            errors.append(f"Job {i + 1} is not assigned to any machine.")

    # Calculate penalties and validate
    for job_index in range(num_jobs):
        delay = max(0, job_completion_times[job_index] - deadlines[job_index])
        penalty = weights[job_index] * delay
        total_penalty += penalty

    if total_penalty != expected_penalty:
        errors.append(f"Calculated penalty ({total_penalty}) does not match the expected value ({expected_penalty}).")

    return errors, total_penalty

def main(instance_file, solution_file):
    n, p, w, d = read_instance(instance_file)
    expected_penalty, schedule = read_solution(solution_file)

    errors, calculated_penalty = validate_solution(n, p, w, d, expected_penalty, schedule)

    print(f"Given penalty: {expected_penalty}")
    print(f"Calculated penalty: {calculated_penalty}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f" - {error}")
    else:
        print("Solution is valid.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 validator.py <instance> <solution>")
        sys.exit(1)

    # for i in range(50, 501, 50):
    #     instance_file = f"instancje/in_151868_{i}.txt"
    #     solution_file = f"pliki_wynikowe/out_{i}"
    #     main(instance_file, solution_file)
    
    instance_file = sys.argv[1]
    solution_file = sys.argv[2]
    main(instance_file, solution_file)
