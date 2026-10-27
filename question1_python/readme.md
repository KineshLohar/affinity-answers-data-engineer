# MD Computers Product Scraper

A Python web scraper that searches for products on [MD Computers](https://mdcomputers.in/), extracts product details, and saves the results to a CSV file.

## 1. Features

- Accepts a product search term from the user.
- Retrieves the product search page.
- Extracts product names, product URLs, original prices, and discounted prices.
- Saves successfully extracted results to a CSV file with a user-provided filename.
- Handles HTTP errors, connection failures, empty search terms, and CSV file errors.
- Uses separate functions for fetching, parsing, and saving data to keep the code readable and maintainable.

## 2. Technology Stack

- **Python 3.14** — main programming language.
- **Requests (`curl_cffi`)** — sends HTTP requests with Chrome browser impersonation.
- **Beautiful Soup 4** — parses HTML and extracts product information.
- **CSV module** — saves the extracted products in CSV format.
- **Pathlib** — handles output file paths.

## 3. Prerequisites

Install Python 3.14 or a compatible Python version and ensure it is available from your terminal.

Verify the installation:

```bash
python --version
```

The project uses the following third-party packages:

- `curl_cffi`
- `beautifulsoup4`

## 4. Installation and Setup

### Step 1: Open the project directory

Open PowerShell or a terminal and navigate to the folder containing `scraper.py`.

cd path\to\question1_python

Replace the example path with your actual project directory.

### Step 2: Create a virtual environment

python -m venv .venv


### Step 3: Activate the virtual environment

In terminal or powershell, first activate our virtual environment

.\.venv\Scripts\Activate.ps1

### Step 4: Install dependencies

Install the required packages:

python -m pip install requirements.txt

### Step 5: Run the scraper

python scraper.py

## 5. How to Use the Scraper

When the program starts, it asks for two inputs.

**Input 1: Product search term**

For example:

Enter a product search term: external hard drives

**Input 2: Output CSV filename**

For example:

Enter the output CSV filename: external_hard_drives.csv

If the request succeeds and product details are extracted, the program creates the CSV file and displays the number of products extracted and the output file path.


## 6. Output Format

The CSV file contains the following columns:

| Column | Description |
|---|---|
| `name` | Product name |
| `url` | Product page URL |
| `original_price` | Original product price, if available |
| `discounted_price` | Discounted product price, if available |

Example output:

```csv
name,url,original_price,discounted_price
"Example Product","https://example.com/product","₹1,299","₹550"
```

The example row is illustrative and is not a live product result.

The output is saved using UTF-8 with a byte-order mark to improve compatibility with spreadsheet applications such as Microsoft Excel.

## 7. Implementation Approach

The scraper is divided into three main functions.

### 7.1 Fetching the search page

`fetch_search_page(search_term)`

- Constructs the search URL and query parameters.
- Sends the HTTP request using `curl_cffi`.
- Uses Chrome browser impersonation through `impersonate="chrome"`.
- Applies a request timeout.
- Checks the HTTP response status.
- Converts HTTP and connection errors into readable application errors.

### 7.2 Extracting product details

`extract_products(html)`

- Parses the returned HTML using Beautiful Soup.
- Locates product cards using CSS selectors.
- Extracts product names and URLs.
- Extracts original and discounted prices when present.
- Skips cards that do not contain a product name or link.
- Returns the extracted products as a list of dictionaries.

Separating HTML parsing from HTTP requests also allows the parser to be tested independently using saved HTML samples.

### 7.3 Saving the results

`save_products_to_csv(products, filename)`

- Normalizes the output filename to use the `.csv` extension.
- Creates the output directory if necessary.
- Writes the column headers and product records.
- Returns the resolved output file path.

The program only attempts to save results when the request succeeds and products have been extracted.

## 8. Challenges Faced and Solutions

### Challenge 1: Cloudflare blocked the initial request

The initial implementation used the standard `requests` library. MD Computers returned an HTTP `403 Forbidden` response with a Cloudflare challenge page instead of the expected product search HTML.

This prevented the parser from receiving the actual product cards.

### Solution: Change the HTTP client

I investigated alternative HTTP client options and changed the implementation to use `curl_cffi`.

The updated request uses:

```python
response = requests.get(
    url,
    params=params,
    headers=headers,
    impersonate="chrome",
    timeout=20,
)
```

Here, `requests` refers to the interface imported from `curl_cffi`, not the standard Requests library.

The `impersonate="chrome"` option configures browser-like TLS and HTTP behavior. In my testing, this approach allowed the request to retrieve the product page and enabled the parser to extract product details.

Browser impersonation is not guaranteed to work against every Cloudflare configuration, and it does not replace permission to automate access to a website.

### Challenge 2: Hardcoded search terms

Initially, the search term was fixed in the code. This meant that changing the product required editing the source file.

### Improvement: Accept runtime inputs

The program now asks the user for a search term and output filename. This makes the scraper reusable for different product searches without modifying the code.

### Challenge 3: Making the results reusable

Printing extracted products to the terminal alone would make them difficult to inspect, sort, or use in another application.

### Improvement: Export to CSV

The scraper now saves product details in CSV format. The results can be opened in Excel or imported into other data-processing tools.

### Challenge 4: Error handling

Network failures, HTTP errors, and file-writing errors can interrupt scraping.

The implementation handles these cases and displays readable error messages instead of exposing an unhandled exception to the user.

## 9. Testing

The HTML parser was tested using a saved product-card HTML sample.

The tests cover:

- Extracting product details from a product card.
- Extracting multiple products from one page.
- Handling empty HTML.
- Handling HTML without product cards.
- Handling products that do not have prices.

Run the test suite from the project directory:

```powershell
python -m unittest discover -s tests -v
```

The five parser tests passed during development.

These tests validate the parsing logic against local HTML fixtures. They do not independently guarantee that the live website will remain accessible or that every product-page layout will use the same HTML structure.

## 10. Limitations and Future Improvements

- **Website changes:** CSS selectors may need updates if MD Computers changes its page structure.
- **Access restrictions:** The website may block automated requests, and browser impersonation may not always work.
- **Pagination:** The current implementation extracts products from the returned page; it does not automatically navigate through multiple result pages.
- **Price formats:** Prices are preserved as displayed strings rather than converted to numeric values.
- **Testing:** Additional tests could cover malformed HTML, missing URLs, unexpected price structures, and CSV-writing failures.
- **Politeness and access:** Requests should respect the website's terms, access restrictions, and any applicable crawling policies.

## 11. Use of AI Assistance

I used ChatGPT and Codex as development assistants while building this scraper.

AI assistance helped with:

- Structuring the Python implementation.
- Identifying appropriate Beautiful Soup CSS selectors.
- Implementing HTTP request handling and error messages.
- Investigating the HTTP 403 issue and evaluating alternative HTTP client options.
- Adding user input and CSV export functionality.
- Writing and running unit tests for the HTML parser.

I iteratively tested the code, inspected the returned HTML, and refined the implementation based on the observed behavior.

AI was used as a development aid; the implementation and its limitations were evaluated through testing rather than assuming that generated code would work without verification.

## 12. Summary

This project demonstrates a basic web-scraping workflow: requesting a product search page, parsing HTML, extracting structured data, handling request errors, and exporting results to CSV.

The implementation evolved from a simple HTML parser into a command-line scraper with configurable inputs, file output, and separate functions for fetching, extraction, and saving.

The primary challenge was the initial HTTP 403 response. Switching to `curl_cffi` with Chrome impersonation improved the ability to retrieve the page during development, while unit tests helped validate the extraction logic independently.
