import csv
import statistics
import argparse

def calculate_statistics(csv_file):
    metrics = {
        "Startup Time 1": [],
        "Startup Time 2": [],
        "Execution Time": [],
        "Creation Time": []
    }

    student_value_tables = 2.0423

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            for metric, value in row.items():
                if metric in metrics:
                    metrics[metric].append(parse_time(value))

    calculated_statistics = {}
    for metric, values in metrics.items():
        avg = statistics.mean(values)
        std_dev = statistics.stdev(values)
        t_student_value = student_value_tables * std_dev
        left = avg - student_value_tables * std_dev
        right = avg + student_value_tables * std_dev
        calculated_statistics[metric] = [avg, std_dev, t_student_value, left, right]
    return calculated_statistics

def parse_time(time_str):
    components = time_str.split(":")
    return int(components[0]) * 3600 + int(components[1]) * 60 + float(components[2])

def write_statistics_to_csv(statistics, output_file):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Average", "Std Dev","T-Student Value","Left", "Right"])
        for metric, values in statistics.items():
            writer.writerow([metric, *values])
    print(f"Statistics saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Calculate statistics and update a CSV file")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()
    statistics = calculate_statistics(args.csv_file)
    write_statistics_to_csv(statistics, args.output_file)

if __name__ == "__main__":
    main()
