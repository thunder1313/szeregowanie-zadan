import os
import csv
import subprocess
import time
import re

def run_verification_for_all_files(executable, index, results):
    exec_name = os.path.splitext(os.path.basename(executable))[0]
    
    for i in range(50, 501, 50):
        input_file = f'in_151788_{i}.txt'
        output_file = f'out_{index}_{i}.txt'
        exec_output_file = f'out_{exec_name}_{i}.txt'
        
        if os.path.exists(input_file):
            print(f"Running verification for {input_file}")
            try:
                start_time = time.time()
                command = ['python', 'weryfikator_czasu.py', executable, input_file, output_file, str(i//10)]
                print(f"Executing command: {' '.join(command)}")
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                if result.returncode != 0:
                    print(f"Error running verification for {input_file}. Return code: {result.returncode}")
                    print(f"Error output: {result.stderr}")
                    value = "Error"
                else:
                    print(f"Verification completed for {input_file}.")
                    print(f"Output: {result.stdout}")
                    exec_command = ['python3', 'weryfikator.py', input_file, output_file]
                    exec_result = subprocess.run(
                        exec_command,
                        capture_output=True,
                        text=True
                    )
                    if exec_result.returncode != 0:
                        print(f"Error running weryfikator.py for {exec_output_file}. Return code: {exec_result.returncode}")
                        print(f"Error output: {exec_result.stderr}")
                        value = "Error"
                    else:
                        print(f"Verification completed for {exec_output_file}.")
                        print(f"Output: {exec_result.stdout}")
                        with open(output_file, 'r') as f:
                            value = f.readline().strip()

                if i not in results:
                    results[i] = {}
                results[i][index] = (elapsed_time, value)

            except Exception as e:
                print(f"Exception occurred while running verification for {input_file}: {e}")
                if i not in results:
                    results[i] = {}
                results[i][index] = (None, "Exception")
        else:
            print(f"Input file {input_file} does not exist. Skipping.")
            if i not in results:
                results[i] = {}
            results[i][index] = (None, "File not found")

if __name__ == "__main__":
    indexes = ['151796', '151840', '151891', '151868', '151059', '151805', '151788', '151892', '153933', '152948', '151850', '152040', '151920', '152094']

    results = {}

    for index in indexes:
        executable = index + '.exe'
        run_verification_for_all_files(executable, index, results)

    with open('times.csv', 'w', newline='') as timesfile, open('values.csv', 'w', newline='') as valuesfile:
        times_writer = csv.writer(timesfile, delimiter=';')
        values_writer = csv.writer(valuesfile, delimiter=';')
        
        times_header = ['Instances'] + [f'{index}_time' for index in indexes]
        values_header = ['Instances'] + [f'{index}_value' for index in indexes]
        times_writer.writerow(times_header)
        values_writer.writerow(values_header)
        
        for instance_size in sorted(results.keys()):
            times_row = [instance_size]
            values_row = [instance_size]
            for index in indexes:
                elapsed_time, value = results[instance_size].get(index, ('', ''))
                times_row.append(elapsed_time)
                values_row.append(value)
            times_writer.writerow(times_row)
            values_writer.writerow(values_row)