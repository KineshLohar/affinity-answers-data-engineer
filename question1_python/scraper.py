import csv
from pathlib import Path

from curl_cffi import requests
from bs4 import BeautifulSoup


def fetch_search_page(search_term):
    """Fetch the MD Computers search results page using browser impersonation."""
    url = "https://mdcomputers.in/"

    params = {
        "route": "product/search",
        "search": search_term,
    }

    # Clean, modern headers that match a real Chrome browser instance
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not A(User%20Arbrand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    try:
        # Crucial addition: impersonate="chrome" tells curl_cffi to spoof TLS & HTTP/2 fingerprints
        response = requests.get(
            url,
            params=params,
            headers=headers,
            impersonate="chrome",  
            timeout=20,
        )
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        raise RuntimeError(
            f"MD Computers returned HTTP {status_code}. "
            "The search page could not be retrieved. (Cloudflare might be blocking it)"
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Could not connect to MD Computers: {error}"
        ) from error


def extract_products(html):
    """Extract product details from search-result HTML."""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    cards = soup.select(
        ".retrinapro-productlist-all_products_design "
        ".product-grid-item"
    )

    for card in cards:
        name_element = card.select_one(
            "h3.product-entities-title a"
        )

        if name_element is None:
            continue

        price_element = card.select_one("span.price")

        original_price = None
        discounted_price = None

        if price_element:
            original = price_element.select_one(".del .amount")
            discounted = price_element.select_one(".ins .amount")

            if original:
                original_price = original.get_text(
                    " ", strip=True
                )

            if discounted:
                discounted_price = discounted.get_text(
                    " ", strip=True
                )

        products.append({
            "name": name_element.get_text(" ", strip=True),
            "url": name_element.get("href"),
            "original_price": original_price,
            "discounted_price": discounted_price,
        })

    return products


def save_products_to_csv(products, filename):
    """Save extracted products to a CSV file."""
    output_path = Path(filename).expanduser()

    if output_path.suffix.lower() != ".csv":
        output_path = output_path.with_suffix(".csv")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "name",
        "url",
        "original_price",
        "discounted_price",
    ]

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(products)

    return output_path.resolve()


def main():
    """Run the scraper and save successful results."""
    search_term = input(
        "Enter a product search term: "
    ).strip()

    if not search_term:
        print("Error: Search term cannot be empty.")
        return

    filename = input(
        "Enter the output CSV filename: "
    ).strip()

    if not filename:
        print("Error: Output filename cannot be empty.")
        return

    try:
        html = fetch_search_page(search_term)
    except RuntimeError as error:
        print(f"Error: {error}")
        print("No output file was created.")
        return

    products = extract_products(html)

    if not products:
        print("No products were found in the returned HTML.")
        print("No output file was created.")
        return

    try:
        output_path = save_products_to_csv(products, filename)
    except OSError as error:
        print(f"Could not save the CSV file: {error}")
        return

    print(f"\nProducts extracted: {len(products)}")
    print(f"CSV saved successfully: {output_path}")


if __name__ == "__main__":
    main()
