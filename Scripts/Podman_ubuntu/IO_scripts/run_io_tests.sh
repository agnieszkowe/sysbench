#!/bin/bash

for ((i=1; i<=30; i++)); do
    OUTPUT_FILE="exp_${i}.txt"
    OUTPUT_DIR="IO_tests/"

    echo "Running tests for EXPERIMENT=$i..."
            
    (time podman-compose up | tee "${OUTPUT_DIR}/${OUTPUT_FILE}")

    podman rm -f $(podman ps -a -q)
            
    echo "Tests for EXPERIMENT=$i completed."
    echo ""
done
