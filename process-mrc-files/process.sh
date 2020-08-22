#!/bin/bash

# Script Parameters
name_pos=${1:-0}
deg_pos=${2:-3}
sep=${3:-'_'}

# Generate Output Directories
mkdir duplicates
mkdir stack-out
mkdir log
mkdir backup

files=(./*.mrc)

file_1=${files[0]}

IFS=$sep read -ra names <<<"$file_1"
min="${names[$deg_pos]}"
max="${names[$deg_pos]}"

for ((i = 1; i < ${#files[@]}; ++i)); do
    file_2=${files[$i]}

    IFS=$sep read -ra names_1 <<<"$file_1"
    IFS=$sep read -ra names_2 <<<"$file_2"

    # Find duplicates
    if [ "${names_1[$name_pos]}" == "${names_2[$name_pos]}" -a "${names_1[$deg_pos]}" == "${names_2[$deg_pos]}" ]; then
        mv $file_1 ./duplicates
        echo "Find duplicate: $file_1" >>log/duplicates.txt

        file_1=$file_2
        continue
    fi

    if [ "${names_1[$name_pos]}" == "${names_2[$name_pos]}" ]; then
        # Update the maximum and minimum
        if (($(echo "${names_1[$deg_pos]} > ${names_2[$deg_pos]}" | bc -l))); then
            min="${names_2[$deg_pos]}"
        fi
        if (($(echo "${names_1[$deg_pos]} < ${names_2[$deg_pos]}" | bc -l))); then
            max="${names_2[$deg_pos]}"
        fi
    else
        # Process the group of data
        echo "${names_1[$name_pos]},${min},${max}" >>log/ranges.txt
        newstack $(ls ${names_1[$name_pos]}_* | sort -nr -k 4 -t '_') "stack-out/${names_1[$name_pos]}.mrc"
        sh -c "mv ${names_1[$name_pos]}_* ./backup"

        max="${names_2[$deg_pos]}"
        min="${names_2[$deg_pos]}"
    fi

    file_1=$file_2
done

# Process the last group of data
IFS=$sep read -ra names <<<"$file_1"
echo "${names[$name_pos]},${min},${max}" >>log/ranges.txt
newstack $(ls ${names[$name_pos]}_* | sort -nr -k 4 -t '_') "stack-out/${names[$name_pos]}.mrc"
sh -c "mv ${names[$name_pos]}_* ./backup"
