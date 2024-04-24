import subprocess
import json
import datetime
import pytz
import argparse
import csv

def run_and_inspect_container(container_image):
    try:
        container_name = "test_container" 
        subprocess.run(["podman", "run", "-d", "--name", container_name, "--rm=false", container_image, "sh", "-c", "echo 'Container test_container is running...' && sleep 10"])
        print(f"Container {container_name} is running...")
        subprocess.run(["podman", "wait", container_name])
        print(f"Container {container_name} has finished.")
        result = subprocess.run(["podman", "container", "inspect", container_name], capture_output=True, text=True)
        container_info = json.loads(result.stdout)
        return container_info
    except Exception as e:
        print("Error running, inspecting, or removing container:", e)
        return None

def calculate_real_times(container_info):
    if container_info:
        created_time = datetime.datetime.fromisoformat(container_info[0]["Created"].replace("Z", "+00:00"))
        started_time = datetime.datetime.fromisoformat(container_info[0]["State"]["StartedAt"].replace("Z", "+00:00"))
        finished_time = datetime.datetime.fromisoformat(container_info[0]["State"]["FinishedAt"].replace("Z", "+00:00"))
        startup_time_1 = started_time - created_time
        startup_time_2 = started_time - current_time
        execution_time = finished_time - started_time
        creation_time = created_time - current_time
        return startup_time_1, startup_time_2, execution_time, creation_time

parser = argparse.ArgumentParser(description="Run container tests and save results to a CSV file")
parser.add_argument("container_image", type=str, help="Name of the container image")
parser.add_argument("num_tests", type=int, help="Number of tests to run")
args = parser.parse_args()

container_image = args.container_image
num_tests = args.num_tests

csv_file = f"container_tests_{container_image.replace(':', '_')}.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Test", "Startup Time 1", "Startup Time 2", "Execution Time", "Creation Time"])
    for i in range(num_tests):
        print(f"Test {i + 1}:")
        subprocess.run(["podman", "rm", "--force", "test_container"])
        current_time = datetime.datetime.now(tz=pytz.timezone('Europe/Warsaw')) 
        container_info = run_and_inspect_container(container_image)
        if container_info:
            startup_time_1, startup_time_2, execution_time, creation_time = calculate_real_times(container_info)
            writer.writerow([i + 1, startup_time_1, startup_time_2, execution_time, creation_time])
print(f"Results saved to {csv_file}")