
#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: bash question3.sh <csv_url>" >&2
    exit 1
fi

url="$1"
input_file=$(mktemp)
sorted_file=$(mktemp)
output_file="output.csv"

trap 'rm -f "$input_file" "$sorted_file"' EXIT

# Download the CSV.
if ! curl -fLsS "$url" -o "$input_file"; then
    echo "Error: Failed to download CSV." >&2
    exit 1
fi

# Parse the CSV, preserving quoted commas.
# Intermediate format: year|company|location
awk '
function parse_csv(line, fields,    i, c, nextc, quoted, field, n) {
    delete fields
    quoted = 0
    field = ""
    n = 0

    for (i = 1; i <= length(line); i++) {
        c = substr(line, i, 1)
        nextc = substr(line, i + 1, 1)

        if (c == "\"") {
            if (quoted && nextc == "\"") {
                field = field "\""
                i++
            } else {
                quoted = !quoted
            }
        } else if (c == "," && !quoted) {
            fields[++n] = field
            field = ""
        } else {
            field = field c
        }
    }

    fields[++n] = field
    return n
}

NR == 1 { next }

{
    count = parse_csv($0, f)

    if (count < 8) {
        next
    }

    company = f[2]
    location = f[5]
    founded = f[8]

    if (match(founded, /[0-9][0-9][0-9][0-9]/)) {
        year = substr(founded, RSTART, RLENGTH)
        printf "%s|%s|%s\n", year, company, location
    }
}
' "$input_file" > "$sorted_file"

# Write the final output to a CSV file.

# Generate the final output once, then display and save it.
{
    printf '"Security","Headquarters Location","Founded"\n'

    sort -t'|' -k1,1n -k2,2 "$sorted_file" |
        awk -F'|' '
        function csv_quote(value) {
            gsub(/"/, "\"\"", value)
            return "\"" value "\""
        }

        {
            printf "%s,%s,%s\n",
                csv_quote($2),
                csv_quote($3),
                csv_quote($1)
        }'
} | tee "$output_file"

echo " "
echo "Success! Results saved to: $output_file"
