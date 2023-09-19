#!/bin/bash

# Run nginx

echo "Starting nginx..."
pidof nginx >/dev/null && echo "nginx is already running [ OK ]" || sudo nginx

echo "-----------------------------------------------------------------"
echo "Ready!"
echo "-----------------------------------------------------------------"
