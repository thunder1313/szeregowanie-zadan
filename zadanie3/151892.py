# import sys
# import time

# def read_input(filename):
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         n = int(lines[0].strip())
#         p = []
#         r = []
#         d = []
#         w = []

#         for i in range(1, n + 1):
#             task_data = list(map(int, lines[i].split()))
#             p.append(task_data[:4])
#             r.append(task_data[4])
#             d.append(task_data[5])
#             w.append(task_data[6])

#     return n, p, r, d, w
# #wazne
# # def evaluate_solution(sequences, p, r, d, w):
# #     current_time = [0] * 4
# #     total_penalty = 0
# #     completion_times = [0] * len(sequences[0])

# #     for machine_id, sequence in enumerate(sequences):
# #         for task in sequence:
# #             task_index = task - 1
# #             start_time = max(current_time[machine_id], r[task_index])
# #             completion_time = start_time + p[task_index][machine_id]
# #             current_time[machine_id] = completion_time
# #             completion_times[task_index] = max(completion_times[task_index], completion_time)
    
# #     for task_index in range(len(completion_times)):
# #         if completion_times[task_index] > d[task_index]:
# #             total_penalty += w[task_index]


# #     return total_penalty


# def evaluate_solution(m_matrix, tasks_orders,n, task_times, )
# def find_solution(n, p, r, d, w, time_limit):
#     start_task_time = time.time()
    
#     # Sort tasks by their deadlines
#     tasks = list(range(1, n + 1))
#     tasks.sort(key=lambda task: d[task - 1])
    
#     # Initialize sequences for each machine
#     sequences = [[] for _ in range(4)]
#     current_time = [0] * 4
#     task_completion_times = [0] * n
#     task_on_machines = [[] for _ in range(n)]

#     while tasks:
#         for machine_id in range(4):
#             if not tasks:
#                 break
#             best_task = None
#             best_time = float('inf')
            
#             for task in tasks:
#                 task_index = task - 1
#                 ready_time = max(current_time[machine_id], r[task_index])
#                 if ready_time < best_time:
#                     best_time = ready_time
#                     best_task = task
            
#             if best_task is not None:
#                 task_index = best_task - 1
#                 sequences[machine_id].append(best_task)
#                 task_on_machines[task_index].append(machine_id + 1)
#                 tasks.remove(best_task)
#                 start_time = max(current_time[machine_id], r[task_index])
#                 completion_time = start_time + p[task_index][machine_id]
#                 current_time[machine_id] = completion_time
#                 task_completion_times[task_index] = max(task_completion_times[task_index], completion_time)
        
#         if time.time() - start_task_time > time_limit:
#             print("Time limit exceeded during processing.")
#             break
    
#     for task in range(1, n + 1):
#         for machine_id in range(4):
#             if task not in sequences[machine_id]:
#                 sequences[machine_id].append(task)
#                 task_on_machines[task - 1].append(machine_id + 1)
    
#     best_penalty = evaluate_solution(sequences, p, r, d, w)

#     return best_penalty, sequences, task_on_machines

# def write_output(filename, best_penalty, sequences, task_on_machines, n):
#     with open(filename, 'w') as f:
#         f.write(f"{best_penalty}\n")
        
#         # Write the sequences for each machine
#         for seq in sequences:
#             f.write(" ".join(str(job) for job in seq) + "\n")
        
#         # Write the sequence of machines for each job
#         for job in range(n):
#             f.write(" ".join(str(machine) for machine in task_on_machines[job]) + "\n")

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python algorytm.py <input_file> <output_file> <time_limit>")
#         sys.exit(1)

#     input_file = sys.argv[1]
#     output_file = sys.argv[2]
#     time_limit = int(sys.argv[3])

#     n, p, r, d, w = read_input(input_file)
#     best_penalty, sequences, task_on_machines = find_solution(n, p, r, d, w, time_limit)
#     write_output(output_file, best_penalty, sequences, task_on_machines, n)


import sys
import time

def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        p = []
        r = []
        d = []
        w = []

        for i in range(1, n + 1):
            task_data = list(map(int, lines[i].split()))
            p.append(task_data[:4])
            r.append(task_data[4])
            d.append(task_data[5])
            w.append(task_data[6])

    return n, p, r, d, w

def evaluate_solution(m_matrix, tasks_orders, n, task_times):
    completed_tasks_counter = 0
    m_done_state = [-1 for _ in range(4)]
    m_time_state = [0 for _ in range(4)]
    task_c_times = [[-1, -1, -1, -1] for _ in range(n)]
    is_deadlock = False

    while completed_tasks_counter < n * 4:
        if is_deadlock:
            print("DEADLOCK")
            return False, 0
        is_deadlock = True

        for m in range(4):
            m_number = m + 1
            for m_task in range(0, n):
                task = m_matrix[m][m_task]
                task_index = task - 1
                task_r_time = task_times[task_index][4]
                current_task_full_order = tasks_orders[task_index]
                which_in_order_index = current_task_full_order.index(m_number)

                if m_done_state[m] < m_task:
                    next_subtask_to_execute = task_c_times[task_index].index(-1)
                    if next_subtask_to_execute == which_in_order_index:
                        if m_time_state[m] >= task_r_time:
                            if current_task_full_order[0] == m_number:
                                start_time = m_time_state[m]
                            else:
                                start_time = max(m_time_state[m], task_c_times[task_index][which_in_order_index - 1])
                        else:
                            if current_task_full_order[0] == m_number:
                                start_time = task_r_time
                            else:
                                start_time = max(task_r_time, task_c_times[task_index][which_in_order_index - 1])

                        c_time = start_time + task_times[task_index][m]
                        m_time_state[m] = c_time
                        task_c_times[task_index][which_in_order_index] = c_time
                        completed_tasks_counter += 1
                        m_done_state[m] = m_task
                        is_deadlock = False
                    break

    completion_times = [max(task_c_times[i]) for i in range(n)]
    calculated_criterion_value = 0

    for i in range(n):
        if completion_times[i] > task_times[i][5]:
            calculated_criterion_value += task_times[i][6]

    return calculated_criterion_value

def find_solution(n, p, r, d, w, time_limit):
    start_task_time = time.time()
    tasks = list(range(1, n + 1))
    tasks.sort(key=lambda task: d[task - 1])
    sequences = [[] for _ in range(4)]
    current_time = [0] * 4
    task_completion_times = [0] * n
    task_on_machines = [[] for _ in range(n)]

    while tasks:
        for machine_id in range(4):
            if not tasks:
                break
            best_task = None
            best_time = float('inf')
            
            for task in tasks:
                task_index = task - 1
                ready_time = max(current_time[machine_id], r[task_index])
                if ready_time < best_time:
                    best_time = ready_time
                    best_task = task
            
            if best_task is not None:
                task_index = best_task - 1
                sequences[machine_id].append(best_task)
                task_on_machines[task_index].append(machine_id + 1)
                tasks.remove(best_task)
                start_time = max(current_time[machine_id], r[task_index])
                completion_time = start_time + p[task_index][machine_id]
                current_time[machine_id] = completion_time
                task_completion_times[task_index] = max(task_completion_times[task_index], completion_time)
        
        if time.time() - start_task_time > time_limit:
            print("Time limit exceeded during processing.")
            break
    
    for task in range(1, n + 1):
        for machine_id in range(4):
            if task not in sequences[machine_id]:
                sequences[machine_id].append(task)
                task_on_machines[task - 1].append(machine_id + 1)
    
    task_times = [p[i] + [r[i], d[i], w[i]] for i in range(n)]
    best_penalty = evaluate_solution(sequences, task_on_machines, n, task_times)

    return best_penalty, sequences, task_on_machines

def write_output(filename, best_penalty, sequences, task_on_machines, n):
    with open(filename, 'w') as f:
        f.write(f"{best_penalty}\n")
        
        for seq in sequences:
            f.write(" ".join(str(job) for job in seq) + "\n")
        
        for job in range(n):
            f.write(" ".join(str(machine) for machine in task_on_machines[job]) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python algorytm.py <input_file> <output_file> <time_limit>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])

    n, p, r, d, w = read_input(input_file)
    best_penalty, sequences, task_on_machines = find_solution(n, p, r, d, w, time_limit)
    write_output(output_file, best_penalty, sequences, task_on_machines, n)