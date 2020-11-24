#!/bin/bash

echo "Start"

service nginx start

echo "Started"
tail -f /dev/null
