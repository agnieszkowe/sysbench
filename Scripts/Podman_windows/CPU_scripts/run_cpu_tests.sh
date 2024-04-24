#!/bin/bash

for ((i=1; i<=30; i++)); do
    for NUMER in 1 2 4 8; do
        for MAX_PRIME in 10000 20000 50000; do
            OUTPUT_FILE="containers_${NUMER}_prime_${MAX_PRIME}_exp_${i}.txt"
            OUTPUT_DIR="CPU_tests/${NUMER}/${MAX_PRIME}"

            echo "Running tests for NUMER=$NUMER, MAX_PRIME=$MAX_PRIME, EXPERIMENT=$i..."

            mkdir -p "${OUTPUT_DIR}"
            
            (time MAX_PRIME=$MAX_PRIME podman compose up --scale sysbench-container=$NUMER) 2>&1 | tee "${OUTPUT_DIR}/${OUTPUT_FILE}"

            podman rm -f $(podman ps -a -q)
            
            echo "Tests for NUMER=$NUMER, MAX_PRIME=$MAX_PRIME, EXPERIMENT=$i completed."
            echo ""
        done
    done
done