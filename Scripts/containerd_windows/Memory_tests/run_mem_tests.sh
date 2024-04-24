#!/bin/bash

Operations=('write' 'read')

generate_docker_compose() {
    local THREAD_NUM=$1
    local OPERATION=$2
    cat > docker-compose.yml <<EOF
version: '3'

services:
  sysbench-container:
    image: agnieszkowe/ubuntu_sysbench
    environment:
      - OPERATION=$OPERATION
      - THREAD_NUM=$THREAD_NUM
    command: /bin/bash -c "sysbench memory --memory-oper=${OPERATION} --threads=${THREAD_NUM} run"
EOF
}

for ((i=1; i<=30; i++)); do
    for OPERATION in "${Operations[@]}"; do
        for THREAD_NUM in 1 2 4 8; do
            echo "THREAD_NUM: $THREAD_NUM"
            OUTPUT_FILE="memory_test_${OPERATION}_threads_${THREAD_NUM}_exp_${i}.txt"
            OUTPUT_DIR="Tests/${OPERATION}"

            echo "Running tests for THREADS=$THREAD_NUM, OPERATION=$OPERATION, EXPERIMENT=$i..."

            mkdir -p "${OUTPUT_DIR}"

            generate_docker_compose $THREAD_NUM $OPERATION

            (sudo time nerdctl compose up) 2>&1 | tee "${OUTPUT_DIR}/${OUTPUT_FILE}"

            sudo nerdctl compose down

            echo "Tests for OPERATION=$OPERATION, THREADS=$THREAD_NUM EXPERIMENT=$i completed."
            echo ""
        done
    done
done