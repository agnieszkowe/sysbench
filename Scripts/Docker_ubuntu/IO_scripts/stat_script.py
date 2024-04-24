import os
import re
import csv
from statistics import mean, stdev

def extract_performance_data(log_text):
    lines = log_text.split("\n")
    for line in lines:
        if "9816M" in line:
            words = line.split()
            index_9816M = words.index("9816M")
            seq_output_data = interpret_value(words[index_9816M + 3])   # Sekwencyjne wyjście w bajtach na sekundę
            seq_output_cpu = interpret_value(words[index_9816M + 4])    # Zużycie CPU dla sekwencyjnego wyjścia
            seq_input_data = interpret_value(words[index_9816M + 9])   # Sekwencyjne wejście w bajtach na sekundę
            seq_input_cpu = interpret_value(words[index_9816M + 10])    # Zużycie CPU dla sekwencyjnego wejścia
            random_seeks_data = interpret_value(words[index_9816M + 11])# Losowe wyszukiwania na sekundę
            return {
                "seq_output_b/sec": seq_output_data,
                "seq_output_%CP": seq_output_cpu,
                "seq_input_b/sec": seq_input_data,
                "seq_input_%CP": seq_input_cpu,
                "random_seeks/sec": random_seeks_data
            }
    print("Nie udało się wyodrębnić danych.")
    return None

def interpret_value(value):
    if value.endswith("m"):
        return float(value[:-1]) * 1000000
    elif value.endswith("k"):
        return float(value[:-1]) * 1000
    else:
        return float(value)

def process_files(folder_path, output_file):
    all_data = {key: [] for key in ['seq_output_b/sec', 'seq_output_%CP', 'seq_input_b/sec', 'seq_input_%CP', 'random_seeks/sec']}
    
    for file in os.listdir(folder_path):
        with open(os.path.join(folder_path, file), 'r') as f:
            log_text = f.read()
        file_data = extract_performance_data(log_text)
        if file_data:
            for key, value in file_data.items():
                all_data[key].append(float(value))

    for key, values in all_data.items():
        print(f'{key}: {values}')             
    
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=all_data.keys())
        writer.writeheader()
        writer.writerow({key: mean(values) for key, values in all_data.items()}) #średnie
        writer.writerow({key: stdev(values) for key, values in all_data.items()}) #odchylenie standardowe
        writer.writerow({key: mean(values) - 2.0423 * stdev(values) for key, values in all_data.items()}) #lewy zakres
        writer.writerow({key: mean(values) + 2.0423 * stdev(values) for key, values in all_data.items()}) #prawy zakres
        writer.writerow({key: 2.0423 * stdev(values) for key, values in all_data.items()}) #wartość t-Studenta

if __name__ == "__main__":
    folders = ['Containerd_ubuntu', 'Docker_ubuntu', 'Podman_ubuntu']
    
    for folder_path in folders:
        output_file = f'io_tests_{folder_path}.csv'
        process_files(folder_path, output_file)