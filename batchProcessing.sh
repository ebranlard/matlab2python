#!/bin/bash

# Check if the directory argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Directory argument is required."
    exit 1
fi

# Check if the directory exists
if [ ! -d "$1" ]; then
    echo "Error: Directory does not exist."
    exit 1
fi

# Recursively find all files and execute the command on each file
find "$1" -type f -name "*.m" | while read file; do
    python matlab2python.py "$file" -o "${file%.m}.py"
done

echo "Conversion completed."