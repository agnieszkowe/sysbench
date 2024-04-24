#!/bin/bash

generate_docker_compose() {
    local NUM_CONTAINERS=$1
    local MAX_PRIME=$2
    cat > docker-compose.yml <<EOF
version: '3'

services:
  sysbench-container:
    image: agnieszkowe/ubuntu_sysbench
    environment:
      - MAX_PRIME=$MAX_PRIME
    command: /bin/bash -c "sysbench cpu --cpu-max-prime=\${MAX_PRIME} run"
    deploy:
      replicas: $NUM_CONTAINERS
EOF
}

# Loop over different numbers of containers
for ((i=1; i<=30; i++)); do
    for MAX_PRIME in 10000 20000 50000; do
        for NUMER in 1 2 4 8; do
            OUTPUT_FILE="containers_${NUMER}_prime_${MAX_PRIME}_exp_${i}.txt"
            OUTPUT_DIR="CPU_tests/${NUMER}/${MAX_PRIME}"

            echo "Running tests for NUMER=$NUMER, MAX_PRIME=$MAX_PRIME, EXPERIMENT=$i..."

            mkdir -p "${OUTPUT_DIR}"
            
            generate_docker_compose $NUMER $MAX_PRIME
            
            (time MAX_PRIME=$MAX_PRIME podman-compose up) 2>&1 | tee "${OUTPUT_DIR}/${OUTPUT_FILE}"

            podman-compose down
            
            echo "Tests for NUMER=$NUMER, MAX_PRIME=$MAX_PRIME, EXPERIMENT=$i completed."
            echo ""
        done
    done
done
