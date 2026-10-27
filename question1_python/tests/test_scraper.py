
import unittest
from pathlib import Path

from scraper import extract_products


class TestProductScraper(unittest.TestCase):

    def test_extracts_product_fields(self):
        sample_path = (
            Path(__file__).parent / "sample_product.html"
        )
        html = sample_path.read_text(encoding="utf-8")

        products = extract_products(html)

        self.assertEqual(len(products), 1)

        product = products[0]

        self.assertEqual(
            product["name"],
            "EK-Loop Connect - External USB Cable (1M)",
        )
        self.assertEqual(
            product["url"],
            "https://mdcomputers.in/product/"
            "ek-loop-connect-external-usb-cable",
        )
        self.assertEqual(product["original_price"], "₹1,299")
        self.assertEqual(product["discounted_price"], "₹550")

    def test_empty_html_returns_empty_list(self):
        self.assertEqual(extract_products(""), [])

    def test_html_without_products_returns_empty_list(self):
        html = "<html><body><h1>No products found</h1></body></html>"

        self.assertEqual(extract_products(html), [])

    def test_product_without_price(self):
        html = """
        <div class="retrinapro-productlist-all_products_design">
            <div class="product-grid-item">
                <h3 class="product-entities-title">
                    <a href="https://example.com/product">
                        Test Product
                    </a>
                </h3>
            </div>
        </div>
        """

        products = extract_products(html)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Test Product")
        self.assertIsNone(products[0]["original_price"])
        self.assertIsNone(products[0]["discounted_price"])

    def test_extracts_multiple_products(self):
        html = """
        <div class="retrinapro-productlist-all_products_design">
            <div class="product-grid-item">
                <h3 class="product-entities-title">
                    <a href="https://example.com/product-1">
                        Product One
                    </a>
                </h3>
            </div>

            <div class="product-grid-item">
                <h3 class="product-entities-title">
                    <a href="https://example.com/product-2">
                        Product Two
                    </a>
                </h3>
            </div>
        </div>
        """

        products = extract_products(html)

        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]["name"], "Product One")
        self.assertEqual(products[1]["name"], "Product Two")

if __name__ == "__main__":
    unittest.main()
