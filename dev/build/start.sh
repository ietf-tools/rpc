#!/bin/bash
#
# Environment config:
#
#  CONTAINER_ROLE - backend or migrations
#
case "${CONTAINER_ROLE:-backend}" in
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
