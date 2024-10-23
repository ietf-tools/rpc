#!/bin/bash
#
# Environment config:
#
#  CONTAINER_ROLE - frontend, backend, or migrations
#
case "${CONTAINER_ROLE:-backend}" in
    frontend)
        exec ./frontend-start.sh
        ;;
    backend)
        exec ./backend-start.sh
        ;;
    migrations)
        exec ./migration-start.sh
        ;;
    *)
        echo "Unknown role '${CONTAINER_ROLE}'"
        exit 255
esac
