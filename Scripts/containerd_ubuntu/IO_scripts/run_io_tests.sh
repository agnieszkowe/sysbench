#!/bin/bash

for ((i=1; i<=30; i++)); do
    OUTPUT_FILE="exp_${i}.txt"
    OUTPUT_DIR="IO_tests/"

    echo "Running tests for EXPERIMENT=$i..."
            
    (time nerdctl compose -f docker-compose.yml up | tee "${OUTPUT_DIR}/${OUTPUT_FILE}")

    sudo nerdctl rm -f $(sudo nerdctl ps -a -q)
            
    echo "Tests for EXPERIMENT=$i completed."
    echo ""
done
