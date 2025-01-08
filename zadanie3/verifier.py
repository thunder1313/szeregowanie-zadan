import csv
import sys

def verify_output_file(input_file, output_file):
    with open(input_file, "r") as f:
        input_lines = f.readlines()

    with open(output_file, "r") as f:
        output_lines = f.readlines()

    task_times = [list(map(int, line.strip().split())) for line in input_lines[1:]]  # tablica zadań z pliku wejściowego, każdy wiersz zawiera 7 wartości, p1, p2, p3, p4, r, d, w
    n = int(input_lines[0].strip())  # wielkość instancji

    m_lines = output_lines[1:5]
    m_matrix = []  # macierz zawierająca kolejność wykonywania zadań na poszczególnych maszynach
    tasks_orders = []  # macierz zawierająca n wierszy po 4 kolumny, zawierająca dla i-tego wiersza (auta) kolejność odwiedzanych stacji (maszyn)
    criterion_value = int(output_lines[0].strip())  # kryterium z algorytmu
    calculated_criterion_value = 0  # obliczone kryterium

    # sprawdzanie, czy każdy z 4 wierszy macierzy zawiera n wartości z zakresu od 1 do n
    m_c = 1
    for line in m_lines:
        tasks_on_station = list(map(int, line.strip().split()))
        m_matrix.append(tasks_on_station)
        if len(tasks_on_station) > n:
            return -1, -1, False, f"Na stacji {m_c} jest więcej zadań niż oczekiwano - któryś samochód odwiedził więcej stacji niż powinien lub pojawił się samochód o błędnym numerze"
        if len(tasks_on_station) < n:
            return -1, -1, False, f"Na stacji {m_c} jest mniej zadań niż oczekiwano - któryś samochód nie odwiedził wszystkich stacji"
        if sorted(tasks_on_station) != list(range(1, n + 1)):
            return -1, -1, False, f"Każdy wiersz macierzy musi zawierać liczby od 1 do n - istenieje auto o złym numerze na stacji {m_c}"
        m_c+=1

    # sprawdzanie czy plik wynikowy ma n wierszy z kolejnością wykonywania podprocesów dla danego procesu
    tasks_order_lines = output_lines[5:5 + n]
    if len(tasks_order_lines) != n:
        return -1, -1, False, "w pliku musi występować n wierszy z kolejnoścami subzadań w ramach zadania"

    # sprawdzanie czy każdy proces składa się z 4 podprocesów od 1 do 4
    l_c = 1
    for line in tasks_order_lines:
        order = list(map(int, line.strip().split()))
        tasks_orders.append(order)
        if set(order) != {1, 2, 3, 4}:
            return -1, -1, False, f"Auto {l_c} nie zawiera poprawnej kolejność odwiedzania stacji. Musi zawierać liczby 1, 2, 3, 4 w dowolnej kolejności"
        l_c += 1


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

        for m in range(4):  # stanowisko
            m_number = m + 1

            for m_task in range(0, n):
                task = m_matrix[m][m_task]
                task_index = task - 1
                task_r_time = task_times[task_index][4]
                current_task_full_order = tasks_orders[task_index]  # lista kolejności dla danego zadania

                which_in_order_index = current_task_full_order.index(m_number)  # określa jako które powinno zostać wykonane zadanie na tej maszynie
                # print(task, task_index, task_r_time, current_task_full_order, which_in_order_index, m_done_state[m] < m_task)

                if m_done_state[m] < m_task: # czy obecne zadanie na danej maszynie jest jeszcze do wykonania

                    next_subtask_to_execute = task_c_times[task_index].index(-1)
                    # sprawdza czy podzadanie, które próbujemy wykonać jest podzadaniem, którego nadeszła kolej w ramach zadania
                    if next_subtask_to_execute == which_in_order_index:
                        # print(task, task_index, task_r_time, current_task_full_order, which_in_order_index, current_task_full_order)
                        if m_time_state[m] >= task_r_time:  # nasz task jest ready w obecnym momencie
                            if current_task_full_order[0] == m_number:  # i jest pierwszy w kolejności do wykonania
                                start_time = m_time_state[m]  # to czas rozpoczęcia task to obecny moment czasu dla danej maszyny
                            else:  # i nie jest pierwszy w kolejności
                                # to czas rozpoczęcia jest równy maximum z obecnego momentu maszyny oraz C poprzedzającego go zadania
                                start_time = max(m_time_state[m], task_c_times[task_index][which_in_order_index - 1])
                        else:  # nasze zadanie nie jest ready
                            if current_task_full_order[0] == m_number:
                                start_time = task_r_time  # to czas rozpoczęcia task to ready time
                            else:  # i nie jest pierwszy w kolejności
                                # to czas rozpoczęcia jest równy maximum z obecnego momentu maszyny oraz C poprzedzającego go zadania
                                start_time = max(task_r_time, task_c_times[task_index][which_in_order_index - 1])

                        c_time = start_time + task_times[task_index][m]
                        m_time_state[m] = c_time
                        task_c_times[task_index][which_in_order_index] = c_time
                        completed_tasks_counter += 1
                        m_done_state[m] = m_task
                        is_deadlock = False

                    break

  

    completion_times = [max(task_c_times[i]) for i in range(n)]

    for i in range(n):
        if completion_times[i] > task_times[i][5]:
            calculated_criterion_value += task_times[i][6]


    if calculated_criterion_value == criterion_value:
        
        return criterion_value, calculated_criterion_value, True, "OK!!!"
    else:
        return criterion_value, calculated_criterion_value, False, "Wartości kryteriów się nie zgadzają - prawdopodobnie wystąpiło zrównoleglenie"

def main(instance_file, solution_file):
    expected_value, got_value,error, error_message = verify_output_file(instance_file, solution_file)
    if error:
        print(f"- {error_message}")
    else:
        print("Correct solution")

    print(f"Correct value: {expected_value}")
    print(f"Solution value: {got_value}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python weryfikator_dostany.py <instance> <output>")
        sys.exit(1)

    instance_file = sys.argv[1]
    solution_file = sys.argv[2]
    main(instance_file, solution_file)
    # results = []
    # for i in range(50, 500, 50):
    #     instance_file = f"in_151892_{i}.txt"
    #     output_file = f"out_151892_{i}.txt"
    #     expected_value, got_value,error, error_message = verify_output_file(instance_file, output_file)
    #     results.append((expected_value, got_value, error_message))
    #     with open("end.csv", "w", newline='') as csvfile:
    #         csvwriter = csv.writer(csvfile)
    #         csvwriter.writerow(["Expected Value", "Obtained Value", "Error Message"])
    #         csvwriter.writerows(results)
