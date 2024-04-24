import os
import re
import csv
from statistics import mean, stdev

def get_info(content):
    patterns = {
        'events per second': r'events per second:\s+(\d+\.\d+)',
        'total number of events': r'total number of events:\s+(\d+)',
        'total time': r'total time:\s+(\d+\.\d+)',
        'average': r'avg:\s+(\d+\.\d+)'
    }
    data = {key: [] for key in patterns}
    
    for line in content:
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                data[key].append(float(match.group(1)))
    return data

def process_files(folder_path, output_file):
    all_data = {key: [] for key in ['events per second', 'total time', 'total number of events', 'average']}
    
    for file in os.listdir(folder_path):
        with open(os.path.join(folder_path, file), 'r') as f:
            content = f.readlines()
        file_data = get_info(content)
        for key, value in file_data.items():
            all_data[key].extend(value)
    
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=all_data.keys())
        writer.writeheader()
        writer.writerow({key: mean(values) for key, values in all_data.items()}) #srednie
        writer.writerow({key: stdev(values) for key, values in all_data.items()}) #odchylenie standardowe
        writer.writerow({key: mean(values) - 2.0423 * stdev(values) for key, values in all_data.items()}) #left
        writer.writerow({key: mean(values) + 2.0423 * stdev(values) for key, values in all_data.items()}) #right
        writer.writerow({key: 2.0423 * stdev(values) for key, values in all_data.items()}) #t_student_value

if __name__ == "__main__":
    prefixes = ['1', '2', '4', '8']
    suffixes = ['10000', '20000', '50000']
    
    for prefix in prefixes:
        for suffix in suffixes:
            folder_path = f'CPU_tests/{prefix}/{suffix}'
            output_file = f'{folder_path}/wyniki_{prefix}_{suffix}.csv'
            process_files(folder_path, output_file)
