# Question 3 — Unix Shell Scripting


## IMPORTANT
Although I haven't worked much with Bash before, I still made an effort to understand the problem and develop a solution.

I used AI tools such as ChatGPT and Codex as learning and development assistants rather than simply asking them to generate the final solution. I approached the challenge interactively, asking the AI to break the problem down into step-by-step questions, explain relevant Bash concepts and syntax, and evaluate my understanding along the way.

I answered each question myself, and the AI provided feedback on whether my answers were correct, along with explanations to help me understand the underlying concepts. I also instructed it not to reveal the complete solution until I explicitly asked for it, so I could learn the relevant concepts and work toward the solution progressively.

This approach helped me explore an unfamiliar scripting language, understand the problem-solving process, and use AI assistance as a learning tool while making my own effort to complete the assignment.

## Overview

This project implements a Bash script that downloads company data from a CSV URL, extracts the required fields, sorts the records by founding year in ascending order, and displays the results in the terminal while saving them to an output file named `output.csv`.

### Objectives

- Accept a CSV URL as a command-line argument.
- Download the CSV data using `curl`.
- Extract the company name, headquarters location, and founding year.
- Sort companies by founding year, from oldest to newest.
- Print the processed results to the terminal.
- Save the same results to `output.csv`.
- Handle download failures and temporary files.

## Technologies Used

- **Bash** — Script execution and workflow orchestration.
- **curl** — Downloading the CSV from a URL.
- **awk** — Parsing fields, extracting years, and formatting output.
- **sort** — Sorting records numerically by founding year.
- **tee** — Displaying the results in the terminal while writing them to a file.

## Prerequisites

On Windows, install [Git for Windows](https://git-scm.com/install/windows) to use Git Bash.

The script requires Bash and the command-line utilities `curl`, `awk`, `sort`, and `tee`.

## How to Run

Open Git Bash in the `question3_unix` project directory.

Run the script by passing the CSV URL as an argument:

```bash
bash question3.sh "YOUR_CSV_URL"
```

Original command used

bash question3.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv?utm_source=chatgpt.com"



Replace `YOUR_CSV_URL` with the URL of the CSV file.

After successful processing, the results will be displayed in the terminal and saved to `output.csv` in the current working directory.

## Implementation Approach

The solution follows these steps:

### 1. Validate the Input

The script checks whether exactly one command-line argument has been provided. If the URL is missing or the argument count is incorrect, it displays usage instructions and exits.

### 2. Download the CSV

The script uses `curl` to retrieve the CSV data from the supplied URL.

The options used enable redirect following, suppress the download progress output, and report HTTP errors. If the download fails, the script reports an error instead of continuing with the processing.

### 3. Create Temporary Files

Temporary files are created to store the downloaded CSV and the intermediate sorted data.

A shell exit trap removes these temporary files when the script finishes, including when it exits after an error.

### 4. Parse the CSV Data

The dataset contains eight columns:

| Column | Field |
|---:|---|
| 1 | Symbol |
| 2 | Security |
| 3 | GICS Sector |
| 4 | GICS Sub-Industry |
| 5 | Headquarters Location |
| 6 | Date added |
| 7 | CIK |
| 8 | Founded |

The script skips the header and extracts the following fields:

- `Security` — Company name
- `Headquarters Location` — Company headquarters
- `Founded` — Founding information

A custom `awk` function processes commas outside quoted fields as delimiters, allowing it to handle common cases where a value contains a quoted comma.

For example:

```csv
MMM,3M,Industrials,Industrial Conglomerates,"Saint Paul, Minnesota",1957-03-04,66740,1902
```

The headquarters value `"Saint Paul, Minnesota"` is treated as a single field rather than two separate fields.

### 5. Extract the Founding Year

The `Founded` field can contain a four-digit year or additional text.

For example:

```text
1902
2013 (1888)
```

The script extracts the first four-digit sequence from the field and uses it as the sorting key.

Consequently, `2013 (1888)` is interpreted as `2013`. This is an implementation assumption and may need adjustment if the assignment expects a different interpretation.

Rows without a four-digit sequence are skipped.

### 6. Prepare Intermediate Records

To make sorting easier, the script rearranges the extracted data into an intermediate format:

```text
1902|3M|Saint Paul, Minnesota
1916|A. O. Smith|Milwaukee, Wisconsin
1888|Example Company|Example Location
```

The founding year is placed first, followed by the company name and headquarters location.

The pipe character (`|`) is used as the intermediate delimiter.

### 7. Sort the Records

The `sort` command sorts the intermediate records numerically by the first field in ascending order.

The numeric sort option ensures that years are compared as numbers rather than ordinary text.

The company name is used as a secondary sort key when founding years are equal.

### 8. Format the Final Output

After sorting, `awk` rearranges the fields into the required order:

1. Security
2. Headquarters Location
3. Founded

The output formatter surrounds values with double quotes and escapes double quotes within field values by doubling them.

### 9. Display and Save the Results

The script uses `tee` to send the final formatted output to both destinations:

- **Terminal:** Displays the CSV header and sorted company records.
- **`output.csv`:** Saves the same output in a CSV file.

This ensures both outputs are generated from the same stream of processed data.

## CSV Parsing Challenge and Limitations

A key challenge in this task is that CSV values can contain commas.

For example:

```csv
Security,Headquarters Location,Founded
3M,"Saint Paul, Minnesota",1902
```

A basic command such as:

```bash
awk -F',' '{ print $2 }'
```

splits fields at every comma. It does not understand CSV quoting rules, so the headquarters value can be split incorrectly.

To address this, the solution uses a custom `awk` parsing function that tracks whether the parser is inside a quoted field. Commas encountered inside quoted fields are treated as part of the value, while commas outside quotes separate fields.

### Remaining Limitations

The implementation is a lightweight parser rather than a complete CSV parser.

- **Embedded newlines:** It assumes each CSV record occupies one physical line. Valid CSV files can contain newlines inside quoted fields, which this implementation does not support.
- **Escaped quotes:** The parser handles doubled quotes inside quoted fields, but it does not validate every possible malformed CSV input.
- **Intermediate delimiter:** The intermediate format uses `|`. Company names or locations containing this character could interfere with sorting and field extraction.
- **Output escaping:** The final formatter handles double quotes, but it assumes the intermediate records have been parsed correctly.
- **Founding-year interpretation:** The first four-digit sequence is selected. Fields containing multiple years may require a more specific rule.
- **Missing founding years:** Rows without a four-digit year are skipped rather than included in the output.
- **HTTP success versus valid data:** A successful download does not guarantee that the response is a valid CSV file. Additional validation could improve robustness.

For general-purpose CSV processing, a standards-compliant CSV parser would be more reliable. This implementation uses Bash and standard Unix utilities to meet the intended scripting approach while documenting the assumptions involved.

## Expected Output

For a dataset containing companies with founding years of 1902, 1916, and 1888, the results would be ordered from oldest to newest:

```csv
"Security","Headquarters Location","Founded"
"Example Company","Example Location","1888"
"3M","Saint Paul, Minnesota","1902"
"A. O. Smith","Milwaukee, Wisconsin","1916"
```

The example is illustrative; actual results depend on the downloaded dataset.

## Conclusion

This solution demonstrates a Bash-based data-processing workflow involving HTTP downloads, CSV field extraction, text transformation, numeric sorting, temporary-file management, and output redirection.

It also documents an important data-engineering consideration: choosing the appropriate parsing strategy depends on the structure and complexity of the source data. The implementation addresses quoted commas in common single-line CSV records while clearly identifying the limitations that remain.
