#!/bin/bash

Operations=('write' 'read')

for ((i=1; i<=30; i++)); do
    for OPERATION in "${Operations[@]}"; do
        for THREAD_NUM in 1 2 4 8; do
            echo "THREAD_NUM: $THREAD_NUM"
            OUTPUT_FILE="memory_test_${OPERATION}_threads_${THREAD_NUM}_exp_${i}.txt"
            OUTPUT_DIR="Tests/${OPERATION}"

            echo "Running tests for THREADS=$THREAD_NUM, OPERATION=$OPERATION, EXPERIMENT=$i..."

            mkdir -p "${OUTPUT_DIR}"
            
            (time OPERATION=$OPERATION THREAD_NUM=$THREAD_NUM docker-compose up) 2>&1 | tee "${OUTPUT_DIR}/${OUTPUT_FILE}"

            docker rm -f $(docker ps -a -q)
            
            echo "Tests for OPERATION=$OPERATION, THREADS=$THREAD_NUM EXPERIMENT=$i completed."
            echo ""
        done
    done
done