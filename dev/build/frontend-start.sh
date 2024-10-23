#!/bin/bash -e

echo "Starting Purple Frontend Server..."

# trap TERM and shut down gunicorn
cleanup () {
    if [[ -n "${node_pid}" ]]; then
        echo "Terminating gunicorn..."
        kill -TERM "${node_pid}"
        wait "${node_pid}"
    fi
}

trap 'trap "" TERM; cleanup' TERM

cd client
NITRO_PORT=3000 node .output/server/index.mjs &
node_pid=$!
wait "${node_pid}"
