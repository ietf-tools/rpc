#!/bin/bash

npm install
npm run generate
mkdir -p .output-static
echo "/ /rpc 301" > .output-static/_redirects
mv .output/public .output-static/rpc
