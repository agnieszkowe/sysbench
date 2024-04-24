#!/bin/bash

for ((i=1; i<=30; i++)); do
    OUTPUT_FILE="network_test_exp_${i}.txt"
    OUTPUT_DIR="Tests/"

    echo "Running tests for EXPERIMENT=$i..."
    
    (podman-compose up) 2>&1 | tee "${OUTPUT_DIR}/${OUTPUT_FILE}"

    podman-compose down
    
    echo "Tests for EXPERIMENT=$i completed."
    echo ""
done