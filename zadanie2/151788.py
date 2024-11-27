import sys

def read_input_file(input_filename):
    """Reads the input file and extracts task durations, deadlines, and penalties."""
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    task_durations = []
    penalties = []
    deadlines = []

    for line in lines[1:]:
        parts = list(map(int, line.strip().split()))
        task_durations.append(parts[:4])  # Durations on 4 machines
        penalties.append(parts[4])       # Task penalty
        deadlines.append(parts[5])       # Task deadline

    return n, task_durations, penalties, deadlines


def assign_tasks(n, task_durations, deadlines, penalties):
    """Assigns tasks to machines minimizing penalties using a greedy heuristic."""
    tasks = list(range(1, n + 1))
    # Sort tasks by a weighted criterion (penalty-to-deadline ratio)
    tasks.sort(key=lambda x: penalties[x - 1] / max(1, deadlines[x - 1]))

    sequences = [[] for _ in range(4)]  # Task lists for each machine
    machine_end_times = [0] * 4         # Track machine finish times

    for task in tasks:
        task_index = task - 1
        # Find the best machine (least added workload) for the task
        best_machine = min(
            range(4),
            key=lambda m: machine_end_times[m] + task_durations[task_index][m]
        )
        sequences[best_machine].append(task)
        machine_end_times[best_machine] += task_durations[task_index][best_machine]

    return sequences


def calculate_penalty(sequences, task_durations, penalties, deadlines):
    """Calculates the total penalty based on task completion times."""
    total_penalty = 0

    for machine_idx, machine_seq in enumerate(sequences):
        current_time = 0
        for task in machine_seq:
            task_idx = task - 1
            duration = task_durations[task_idx][machine_idx]
            deadline = deadlines[task_idx]
            penalty = penalties[task_idx]

            current_time += duration
            delay = max(0, current_time - deadline)
            total_penalty += delay * penalty

    return total_penalty


def write_output(output_filename, penalty, sequences):
    """Writes the penalty and task sequences to the output file."""
    with open(output_filename, 'w') as file:
        file.write(f"{penalty}\n")
        for seq in sequences:
            file.write(" ".join(map(str, seq)) + "\n")


def main(input_file, output_file):
    """Main function to read input, generate schedules, and write output."""
    n, task_durations, penalties, deadlines = read_input_file(input_file)
    sequences = assign_tasks(n, task_durations, deadlines, penalties)
    penalty = calculate_penalty(sequences, task_durations, penalties, deadlines)
    write_output(output_file, penalty, sequences)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <output_file> <time_limit>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])  # Placeholder, unused but kept for compatibility.

    main(input_file, output_file)
