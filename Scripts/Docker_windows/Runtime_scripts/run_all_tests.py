import subprocess
import argparse

def run_tests(images, num_tests):
    try:
        for image_name in images:
            print(f"Running tests for image: {image_name}")
            subprocess.run(["python3", "script.py", image_name, str(num_tests)])
            csv_file = f"container_tests_{image_name}.csv"
            output_file = f"statistics_{image_name}.csv"
            subprocess.run(["python3", "statistics_script.py", csv_file, output_file])
            print(f"Tests and statistics for image {image_name} completed\n")
    except Exception as e:
        print("Error running tests:", e)

def main():
    parser = argparse.ArgumentParser(description="Run tests for specified images and generate statistics")
    parser.add_argument("num_tests", type=int, help="Number of times to run the tests for each image")
    args = parser.parse_args()
    images = ["alpine", "registry", "ubuntu", "debian", "nginx", "mysql"]
    run_tests(images, args.num_tests)

if __name__ == "__main__":
    main()

