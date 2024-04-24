#!/bin/bash

generate_docker_compose() {
    local NUM_CONTAINERS=$1
    local MAX_PRIME=$2
    cat > docker-compose.yml <<EOF
version: '3'

services:
  sysbench-container:
    image: agnieszkowe/ubuntu_sysbench
    command: /bin/bash -c "sysbench cpu --cpu-max-prime=${MAX_PRIME} run"
    deploy:
      replicas: $NUM_CONTAINERS
EOF
}

for ((i=1; i<=30; i++)); do
    for NUMER in 1 2 4 8; do
        for MAX_PRIME in 10000 20000 50000; do
            OUTPUT_FILE="containers_${NUMER}_prime_${MAX_PRIME}_exp_${i}.txt"
            OUTPUT_DIR="CPU_tests/${NUMER}/${MAX_PRIME}"
            TEMP_LOG="temp_log.txt"

            echo "Running tests for NUMER=$NUMER, MAX_PRIME=$MAX_PRIME, EXPERIMENT=$i..."

            mkdir -p "${OUTPUT_DIR}"
            echo "" > "$TEMP_LOG"
            
            generate_docker_compose $NUMER $MAX_PRIME
            (time nerdctl compose -f docker-compose.yml up -d)
            sleep 20
            
            container_ids=$(nerdctl ps -aq)

            for container_id in $container_ids; do
                logs=$(nerdctl logs $container_id)
                echo $logs >>  "$TEMP_LOG"
                echo "Logs for Container $container_id:"
                nerdctl logs $container_id
                echo "-----------------------------------------"
            done
                
            cp "$TEMP_LOG" "${OUTPUT_DIR}/${OUTPUT_FILE}"
                
            for container_id in $container_ids; do
                nerdctl rm $container_id
            done
            
            echo "Tests for NUMER=$NUMER, MAX_PRIME=$MAX_PRIME, EXPERIMENT=$i completed."
            echo ""
        done
    done
done