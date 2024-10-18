#!/bin/bash -e

echo "Starting Purple Frontend Server..."

# trap TERM and shut down gunicorn
cleanup () {
    if [[ -n "${gunicorn_pid}" ]]; then
        echo "Terminating gunicorn..."
        kill -TERM "${gunicorn_pid}"
        wait "${gunicorn_pid}"
    fi
}

trap 'trap "" TERM; cleanup' TERM

cd client
NITRO_PORT=3000 node .output/server/index.mjs
gunicorn_pid=$!
wait "${gunicorn_pid}"
