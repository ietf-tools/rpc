#!/bin/bash
#
# Environment config:
#
#  CONTAINER_ROLE - purple or migrations
#
case "${CONTAINER_ROLE:-purple}" in
    purple)
        exec ./purple-start.sh
        ;;
    migrations)
        exec ./migration-start.sh
        ;;
    *)
        echo "Unknown role '${CONTAINER_ROLE}'"
        exit 255
esac
