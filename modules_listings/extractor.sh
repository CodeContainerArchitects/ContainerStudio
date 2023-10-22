#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file output_file"
    exit 1
fi

# Input and output files
input_file="$1"
output_file="$2"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found."
    exit 1
fi

# Process the input file and extract the first word from each line
while IFS= read -r line; do
    # Use 'cut' command to extract the first word
    first_word=$(echo "$line" | cut -d ' ' -f 1)
    # Append the first word to the output file
    echo "$first_word" >> "$output_file"
done < "$input_file"

echo "First words extracted and saved to '$output_file'."