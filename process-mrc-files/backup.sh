#!/bin/bash

for dir in $(find . -maxdepth 1 -mindepth 1 -type d -printf '%f\n');
do
    if [[ "$dir" == *"_output" ]]; then
        continue
    fi

    output_dir="${dir}_output"
    mkdir -p "$output_dir"

    for file in $(find "$dir" -maxdepth 1 -mindepth 1 -type f -printf '%f\n');
    do
        if [[ "$file" == *"_51.rec" \
                || "$file" == "docking.mod" \
                || "$file" == "premembrane.mod" ]]; then
            cp "${dir}/${file}" "${output_dir}/${file}"
        fi
    done
done